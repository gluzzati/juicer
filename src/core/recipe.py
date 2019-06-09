import yaml

from core import log

REQUIRED_FIELDS = ["steps", "taps"]


def parse_one_recipe(yml):
    tag = "[validating recipe] "
    if not isinstance(yml, dict):
        log.error(tag + "not a valid recipe format " + str(type(yml)))
        return False, None

    recipe_name = list(yml)[0]
    for field in REQUIRED_FIELDS:
        if field not in yml[recipe_name]:
            log.error(tag + "missing field " + field)
            return False, None

    recipe = yml[recipe_name]
    steps = recipe["steps"]
    taps = recipe["taps"]

    for i, step in enumerate(steps):
        tap = step[0]
        if tap not in taps:
            log.error("undefined tap \"" + tap + "\"")
            return False, None
        amount = step[1]
        if not (isinstance(amount, float) or isinstance(amount, int)):
            log.error("error parsing step {}: expecting number - got {}".format(i + 1, str(type(amount))))
            return False, None

    for tapname in taps:
        tapno = taps[tapname]
        if not isinstance(tapno, int):
            log.error("error parsing tap \"{}\": expecting int - got {}".format(tapname, str(type(tapno))))
            return False, None

    out = Recipe()
    out.name = recipe_name
    out.steps = steps
    out.taps = taps

    return True, out


def parse_recipes_list_file(file):
    recipes = []
    with open(file, "r") as fid:
        try:
            yml = yaml.safe_load(fid)
            recipe_list = yml["recipes"]
            for recipe in recipe_list:
                valid, r = parse_one_recipe(recipe)
                if not valid:
                    log.error("invalid recipe")
                    return False
                recipes.append(r)
        except yaml.YAMLError as e:
            log.error("yaml error! couldnt parse " + file)
            log.error("exception: " + str(e))
            return False, None
    return True, recipes


class Recipe:
    class Key:
        steps = "steps"
        taps = "taps"
        name = "name"
        step_tap = "tap"
        step_amount = "amount"

    def __init__(self):
        self.steps = list()
        self.taps = dict()
        self.name = None
