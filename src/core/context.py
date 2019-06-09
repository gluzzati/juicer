from queue import Queue

from core.database import Database
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

    def __init__(self, args):
        self.args = args
        self.valid = True
        self.state = Context.State.UNINIT
        self.gui = GuiProxy()
        self.database = Database()
        self.user = None
        self.scale = Scale()
        self.queue = Queue()

        # todo: dehardcode gpio pins to config file!
        self.relay_board = RelayBoard([
            ["water", 2],
            ["orange", 3],
        ])

        self.recipes = dict()
        self.initialize()
