class Glass:
	def __init__(self):
		self.weight = 0
		self.capacity = 0

class User:
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
