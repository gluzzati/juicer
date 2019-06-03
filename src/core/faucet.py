import time

import yaml

from core import log

REQUIRED_FIELDS = ["steps", "taps"]


def parse(yml):
    tag = "[validating recipe] "
    if not isinstance(yml, dict):
        log.error(tag + "not a valid recipe format " + str(type(yml)))
        return False, None, None, None

    if len(yml) is not 1:
        log.error(tag + "only one recipe per yml file allowed")
        return False, None, None, None

    recipe_name = list(yml)[0]
    for field in REQUIRED_FIELDS:
        if field not in yml[recipe_name]:
            log.error(tag + "missing field " + field)
            return False, None, None, None

    recipe = yml[recipe_name]
    steps = recipe["steps"]
    taps = recipe["taps"]

    for i, step in enumerate(steps):
        tap = step[0]
        if tap not in taps:
            log.error("undefined tap \"" + tap + "\"")
            return False, None, None, None
        amount = step[1]
        if not (isinstance(amount, float) or isinstance(amount, int)):
            log.error("error parsing step {}: expecting number - got {}".format(i + 1, str(type(amount))))
            return False, None, None, None

    for tapname in taps:
        tapno = taps[tapname]
        if not isinstance(tapno, int):
            log.error("error parsing tap \"{}\": expecting int - got {}".format(tapname, str(type(tapno))))
            return False, None, None, None

    return True, recipe_name, steps, taps


def parse_recipe_file(file):
    r = Recipe()
    with open(file, "r") as stream:
        try:
            r.from_ymlfile(stream)
        except yaml.YAMLError as e:
            log.error("yaml error! couldnt parse " + file)
            return False, None
    return True, r


class Recipe:
    def __init__(self):
        self.steps = list()
        self.taps = dict()
        self.name = None

    def from_ymlfile(self, yml):
        ymlfile = yaml.safe_load(yml)
        valid, name, steps, taps = parse(ymlfile)
        if not valid:
            log.error("invalid recipe")
            return False

        self.name = name
        self.steps = steps
        self.taps = taps
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
                    time.sleep(1)
                else:
                    log.error("unknown tap " + tap)

        return True

    pass
