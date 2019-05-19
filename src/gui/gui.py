# import time
# from threading import Thread
#
# from kivy.app import App
# from kivy.uix.floatlayout import FloatLayout
#
from core import log


#
# from PyQt5.QtWebEngineWidgets import *
#
#
# class Gui(FloatLayout):
# 	pass
#
#
# class GuiApp(App):
# 	title = 'Gui'
# 	icon = 'icon.png'
#
# 	def run(self):
# 		try:
# 			super().run()
# 		except Exception as e:
# 			log.error("guiapp crashed with exception " + str(e))
#
# 	def build(self):
# 		return Gui()
#
# 	def on_pause(self):
# 		return True
#
#
class GuiProxy:
	def __init__(self):
		pass

	def update(self, arg):
		log.yay("[GUI]:" + arg)

#
# class GuiThread(Thread):
# 	def __init__(self, queue):
# 		self.queue = queue
# 		self.running = True
# 		super().__init__()
#
# 	def run(self):
# 		while self.running:
# 			try:
# 				# GuiApp().run()
# 				my_web = QWebEngineView()
# 				my_web.load(QUrl("http://free-tutorials.org"))
# 				my_web.show()
# 			except Exception as e:
# 				log.error("gui crashed with exception " + str(e))
# 				log.error("reloading gui in 5s...")
# 				time.sleep(5)
# 		return 0
