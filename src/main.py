#!/usr/bin/python3
import sys
from queue import Queue

from core import log
from core.context import Context
from core.events import Event
from core.reactor import ReactorThread
from rfid.rfid import RfidThread


def main():
	log.loglevel = log.LVL_DBG

	# start
	# - core thread
	# - gui thread
	# - rfid thread

	context = Context(sys.argv)
	context.queue = Queue()

	core_th = ReactorThread(context)
	rfid_th = RfidThread(context.queue)

	try:
		core_th.start()
		rfid_th.start()

		rfid_th.join()
		core_th.join()

	except KeyboardInterrupt:
		evt = Event(Event.SIGINT)
		context.queue.put(evt)

		rfid_th.running = False

	core_th.join()
	rfid_th.join()


if __name__ == "__main__":
	main()
