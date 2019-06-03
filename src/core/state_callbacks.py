import time
from threading import Thread

from core import log
from core.context import Context
from core.events import EventType, create_event, EventKey

SAFETY_TIMEOUT = 5
GUARD = 0.9
INFINITY = float('inf')


class Safety(Thread):
    def __init__(self, relay_board, scale, max, queue):
        self.relay_board = relay_board
        self.scale = scale
        self.max = max
        self.queue = queue
        super().__init__()

    def glass_percent(self):
        weight = self.scale.get_weight()
        percent = weight / self.max * 100
        log.debug("{}% full".format(percent))
        return percent

    def glass_full(self):
        return self.glass_percent() >= (100 * GUARD)

    def run(self):
        elapsed = 0
        DT = 0.1
        while elapsed < SAFETY_TIMEOUT and self.relay_board.pouring() and not self.glass_full():
            time.sleep(DT)
            elapsed += DT

        if self.relay_board.pouring():
            self.relay_board.liquid_off()
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
        timer = Safety(ctx.relay_board, ctx.scale, max, ctx.queue)
        ctx.state = Context.State.POURING
        ctx.faucet.dispense(ctx.recipes[ctx.requested_recipe])
        timer.start()
        return True, None
    else:
        log.warn("glass already full")
        return False, None
