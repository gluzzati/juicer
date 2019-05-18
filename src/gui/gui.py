from threading import Thread

from core import log


class GuiProxy:
	def __init__(self):
		pass

	def update(self, arg):
		log.yay("[GUI]:" + arg)


class GuiThread(Thread):
	def __init__(self, queue):
		self.queue = queue
		super().__init__()

	def run(self):
		# app = QApplication(sys.argv)
		# engine = QQmlApplicationEngine()
		# engine.load("gui/gui.qml")
		# app.exec_()
		pass
