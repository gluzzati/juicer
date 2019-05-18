#!/usr/bin/python3
from RPi import GPIO

from core import log
from core.context import Context
from core.events import Event
from core.reactor import ReactorThread
from core.user import User
from rfid.rfid import RfidThread


def main():
	log.loglevel = log.LVL_DBG

	# start
	# - core thread
	# - gui thread
	# - rfid thread

	context = Context()

	# delete this
	giulio = User()
	giulio.name = "Giulio"
	giulio.tag = 797313096147
	giulio.glass_capacity = 250
	giulio.glass_weight = 280
	context.database.add_user(giulio)

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
	GPIO.cleanup()


if __name__ == "__main__":
	main()
