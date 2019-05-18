from core import log


class Gui:
	def update(self, arg):
		pass


class TextGui(Gui):
	def update(self, arg):
		log.yay("[GUI]:" + arg)
