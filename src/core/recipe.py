import yaml

from core import log

REQUIRED_FIELDS = ["steps"]


def parse_one_recipe(yml):
    tag = "[validating recipe] "
    if not isinstance(yml, dict):
        log.error(tag + "not a valid recipe format " + str(type(yml)))
        return False, None

    for field in REQUIRED_FIELDS:
        if field not in yml:
            log.error(tag + "missing field " + field)
            return False, None

    recipe_name = yml["name"]
    steps = yml["steps"]

    for i, step in enumerate(steps):
        tap = step[0]
        amount = step[1]
        if not (isinstance(amount, float) or isinstance(amount, int)):
            log.error("error parsing step {}: expecting number - got {}".format(i + 1, str(type(amount))))
            return False, None

    out = Recipe()
    out.name = recipe_name
    out.steps = steps

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
                    return False, None
                recipes.append(r)
        except yaml.YAMLError as e:
            log.error("yaml error! couldnt parse " + file)
            log.error("exception: " + str(e))
            return False, None
    return True, recipes


class Recipe:
    class Key:
        steps = "steps"
        name = "name"
        step_tap = "tap"
        step_amount = "amount"

    def __init__(self):
        self.steps = list()
        self.name = None
