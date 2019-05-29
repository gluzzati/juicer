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
