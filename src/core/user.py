class User:
	def __init__(self):
		self.name = "Unknown user"
		self.glass_weight = 0
		self.glass_capacity = 0
		self.tag = 0

	def is_valid(self):
		return True

	def to_string(self):
		return "{}@{} - {}g/{}ml".format(self.name, self.tag, self.glass_weight, self.glass_capacity)
