from core.aws_proxy import AWSProxy
from core.event_handlers import *
from core.events import too_old, evt2json
from core.state_callbacks import *


def get_evt(ctx):
    evt = ctx.queue.get(True)

    if not isinstance(evt, dict) or EventKey.type not in evt:
        log.error("Malformed event " + str(evt))
        return False, None

    log.debug("got evt type: " + evt[EventKey.type])

    if evt[EventKey.type] == EventType.SIGINT:
        ctx.running = False
        return False, None

    return True, evt


class Reactor:
    def __init__(self, context):
        self.ctx = context
        self.ctx.running = True
        self.handlers = dict()
        self.callbacks = dict()
        args = self.ctx.args
        try:
            host = args.host
            rootCAPath = args.rootCAPath
            certificatePath = args.certificatePath
            privateKeyPath = args.privateKeyPath
            clientID = "juicer-backend"
            self.aws_proxy = AWSProxy(host, rootCAPath, certificatePath, privateKeyPath, clientID, self.ctx.queue)
            self.aws_proxy.register()
        except Exception as e:
            log.warn("exc: " + str(e))
            log.warn("no aws parameters passed, skipping amazon registration...")
            self.aws_proxy = None

        self.add_handler(EventType.RFID_DETECTED, rfid_detected_handler)
        self.add_handler(EventType.RFID_REMOVED, rfid_removed_handler)
        self.add_handler(EventType.NEW_USER, new_user_handler)
        self.add_handler(EventType.AUTO_WATEROFF, auto_wateroff_handler)
        self.add_handler(EventType.POUR_REQUESTED, pour_requested_handler)
        self.add_handler(EventType.NEW_RECIPE, new_recipe_handler)


        self.add_statecallback(Context.State.IDLE, on_idle)
        self.add_statecallback(Context.State.GLASS_ON, on_glass_on)
        self.add_statecallback(Context.State.POURING, on_pouring)

    def add_handler(self, evt_type, handler):
        self.handlers[evt_type] = handler

    def add_statecallback(self, state, callback):
        self.callbacks[state] = callback

    def handle(self, evt):
        if self.aws_proxy:
            self.aws_proxy.publish(evt2json(evt))
        if evt[EventKey.type] in self.handlers:
            return self.handlers[evt[EventKey.type]](self.ctx, evt)
        else:
            log.error("unknown event " + evt[EventKey.type])
            return False, None

    def change_state(self, next_state):
        if next_state in self.callbacks:
            return self.callbacks[next_state](self.ctx)
        else:
            log.error("unknown state " + str(next_state))
            return False, None

    def run(self):
        while self.ctx.running:

            ok, evt = get_evt(self.ctx)

            if not ok or too_old(evt):
                continue

            ok, next_state = self.handle(evt)
            ok, res = self.change_state(next_state)

        return 0


class ReactorThread(Thread):
    def __init__(self, context):
        self.ctx = context
        super().__init__()

    def run(self):
        consumer = Reactor(self.ctx)
        consumer.run()
