import yaml

from core import log


class Glass:
    class Key:
        weight = "weight"
        capacity = "capacity"

    def __init__(self):
        self.weight = 0
        self.capacity = 0


class User:
    class Key:
        name = "name"
        glass = "glass"
        tag = "tag"

    def __init__(self):
        self.name = "Unknown user"
        self.glass = Glass()
        self.glass.weight = 0
        self.glass.capacity = 0
        self.tag = 0

    def is_valid(self):
        return True

    def to_string(self):
        return "{}@{} - {}g/{}ml".format(self.name, self.tag, self.glass.weight, self.glass.capacity)


def parse_one_user(yml):
    tag = "[validating user] "
    if not isinstance(yml, dict):
        log.error(tag + "not a valid user format " + str(type(yml)))
        return False, None

    user = User()
    user.glass = Glass()

    try:
        user.name = yml["name"]
        user.tag = yml["tag"]

        glass_capacity = yml["glass"]["capacity"]
        if not isinstance(glass_capacity, int) or isinstance(glass_capacity, float):
            log.error("error parsing glass capacity: expecting number - got {}".format(str(type(glass_capacity))))

        glass_weight = yml["glass"]["weight"]
        if not isinstance(glass_capacity, int) or isinstance(glass_weight, float):
            log.error("error parsing glass weight: expecting number - got {}".format(str(type(glass_weight))))

        user.glass.capacity = glass_capacity
        user.glass.weight = glass_weight

        return True, user

    except yaml.YAMLError as e:
        log.error("error parsing user ")
        log.error("exception: " + str(e))
        return False, None


def parse_user_list_file(file):
    users = []
    with open(file, "r") as fid:
        try:
            yml = yaml.safe_load(fid)
            user_list = yml["users"]
            for user in user_list:
                valid, u = parse_one_user(user)
                if not valid:
                    log.error("invalid recipe")
                    return False
                users.append(u)

        except yaml.YAMLError as e:
            log.error("yaml error! couldnt parse " + file)
            log.error("exception: " + str(e))
            return False, None

    return True, users
