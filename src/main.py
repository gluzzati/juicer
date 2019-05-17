#!/usr/bin/python3
import sys
from queue import Queue
from threading import Thread

from core.context import Context
from core.events import Event
from core.evtconsumer import EvtConsumer
from rfid.rfid import RFID


class CoreThread(Thread):
	def __init__(self, queue):
		self.queue = queue
		super().__init__()

	def run(self):
		context = Context(sys.argv)
		context.queue = self.queue
		consumer = EvtConsumer(context)
		consumer.run()


class RfidThread(Thread):
	def __init__(self, queue):
		self.running = True
		self.rfid = RFID()
		self.queue = queue
		self.tag_present = False
		self.current_tag = None
		super().__init__()

	def dispatch(self, evt):
		self.queue.put(evt)

	def run(self):
		while self.running:
			ok, tag = self.rfid.read_id_no_block()
			detected = tag is not None

			if detected and (not self.tag_present or tag != self.current_tag):
				evt = Event()
				evt.type = Event.RFID_DETECTED
				evt.rfid = tag
				self.dispatch(evt)
			elif detected and tag != self.current_tag:
				evt = Event()
				evt.type = Event.RFID_DETECTED
				self.dispatch(evt)
			elif not detected and self.tag_present:
				evt = Event()
				evt.type = Event.RFID_REMOVED
				self.dispatch(evt)


def main():
	# start
	# - core thread
	# - gui thread
	# - rfid thread
	main_queue = Queue()
	core_th = CoreThread(main_queue)
	threadpool = []
	threadpool.append(RfidThread(main_queue))

	core_th.start()
	for thread in threadpool:
		thread.start()

	core_th.join()

	for thread in threadpool:
		thread.running = False


if __name__ == "__main__":
	main()
