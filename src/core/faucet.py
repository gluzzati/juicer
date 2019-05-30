from core import log


class Recipe:
    def __init__(self):
        self.steps = list()

    def parse(self, yml):
        pass

class Faucet:
    def __init__(self, relay_board):
        self.taps_board = relay_board
        pass

    def dispense(self, recipe):
        if not isinstance(recipe, Recipe):
            log.error("trying to dispense something that is not a recipe " + str(type(recipe)))
            return False
        else:
            for tap, amount in recipe.steps:
                if tap in self.taps_board.relays:
                    self.taps_board.relays[tap].pour(amount)
                else:
                    log.error("unknown tap " + tap)

        return True

    pass

