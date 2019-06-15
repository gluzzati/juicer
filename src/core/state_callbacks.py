import time
from threading import Thread

from core import log
from core.context import Context
from core.events import EventType, create_event, EventKey

SAFETY_TIMEOUT = 60
GUARD = 0.9
INFINITY = float('inf')


def tap_is_on(tap, elapsed, recipe):
    if not tap in recipe.steps:
        log.error("tap not in recipe!")
        return False
    else:
        start = recipe.steps[tap][0]
        duration = recipe.steps[tap][1]
        end = start + duration
        return start < elapsed < end
    pass


def total(recipe):
    tot = 0
    for tap in recipe.steps:
        start = recipe.steps[tap][0]
        duration = recipe.steps[tap][1]
        end = start + duration
        tot = max(tot, end)

    return tot

class DispenseThread(Thread):
    def __init__(self, ctx):
        self.relay_board = ctx.relay_board
        self.recipe = ctx.requested_recipe
        self.ctx = ctx
        super().__init__()
        self.name = "dispense"

    def run(self):
        DT = 0.1
        total_poured = 0
        start = time.time()
        elapsed = 0
        log.info("requested " + self.recipe.name)

        while self.ctx.state == Context.State.POURING:
            time.sleep(DT)
            elapsed = time.time() - start

            for tap in self.recipe.steps:
                if tap_is_on(tap, elapsed, self.recipe):
                    self.relay_board.open(tap)
                else:
                    self.relay_board.close(tap)
                if elapsed > total(self.recipe) or not self.relay_board.pouring():
                    self.relay_board.shut_all()

            if elapsed > total(self.recipe) or not self.relay_board.pouring():
                self.relay_board.shut_all()
                break

        log.info("poured " + str(total_poured) + " CCs")
        evt = create_event(EventType.POUR_COMPLETED)
        evt["recipe"] = self.recipe
        evt["total_poured"] = total_poured
        self.ctx.queue.put(evt)



class SafetyThread(Thread):
    def __init__(self, relay_board, scale, max, queue):
        self.relay_board = relay_board
        self.scale = scale
        self.max = max
        self.queue = queue
        super().__init__()
        self.name = "safety"

    def glass_percent(self):
        weight = self.scale.get_weight()
        percent = weight / self.max * 100
        # log.debug("{}% full".format(percent))
        return percent

    def glass_full(self):
        return self.glass_percent() >= (100 * GUARD)

    def run(self):
        elapsed = 0
        DT = 0.1

        while elapsed < SAFETY_TIMEOUT and not self.glass_full():
            time.sleep(DT)
            elapsed += DT
            if not self.relay_board.pouring():
                break

        if self.relay_board.pouring():
            self.relay_board.shut_all()
            evt = create_event(EventType.AUTO_WATEROFF)
            evt[EventKey.cause] = None
            log.warn("auto off")
            if elapsed > SAFETY_TIMEOUT:
                log.warn("timed out")
                evt[EventKey.cause] = "TIMEOUT"
            if self.glass_full():
                log.warn("glass full")
                evt[EventKey.cause] = "GLASS_FULL"
            self.queue.put(evt)


def on_idle(ctx):
    log.debug("on idle")
    ctx.user = None
    ctx.state = Context.State.IDLE
    return True, None


def on_glass_on(ctx):
    log.debug("on glass on")
    ctx.state = Context.State.GLASS_ON
    return True, None


def on_pouring(ctx):
    log.debug("on pouring")

    try:
        max = ctx.user.glass.capacity + ctx.user.glass.weight
    except AttributeError:  # there's an unknown glass on
        max = INFINITY

    if ctx.onscale < max:
        safety_th = SafetyThread(ctx.relay_board, ctx.scale, max, ctx.queue)
        dispenser_th = DispenseThread(ctx)
        ctx.state = Context.State.POURING
        dispenser_th.start()
        safety_th.start()
        return True, None
    else:
        log.warn("glass already full")
        return False, None
