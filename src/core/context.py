from queue import Queue

from core import log
from core.database import Database
from flow_meter.flowmeter import FlowMeter
from gui.gui import GuiProxy
from relay.relay import RelayBoard
from scale.scale import Scale


class Context:
    class State:
        UNINIT = "UNINIT"
        IDLE = "IDLE"
        GLASS_ON = "GLASS_ON"
        POURING = "POURING"

        ALLOWABLE = [
            UNINIT,
            IDLE,
            GLASS_ON,
            POURING,
        ]

    @staticmethod
    def is_valid_state(state):
        if not isinstance(state, str):
            return False
        return state in Context.State.ALLOWABLE

    def initialize(self):
        self.state = Context.State.IDLE

    def __init__(self, config):
        self.valid = True
        self.config = config
        self.state = Context.State.UNINIT
        self.gui = GuiProxy()
        self.database = Database()
        self.queue = Queue()
        self.user = None

        self.scale = Scale(config)
        self.relay_board = RelayBoard(config)
        self.flowmeter = FlowMeter(config)

        self.recipes = dict()
        self.initialize()

    def add_recipe(self, recipe):
        for step in recipe.steps:
            tap = step[0]
            if tap not in self.relay_board.relays:
                log.error("error adding recipe " + recipe.name + ": unknown tap \"" + tap + "\"")
                return False

        self.recipes[recipe.name] = recipe
        return True
