#!/usr/bin/python3
from RPi import GPIO

from core import log
from core.context import Context
from core.events import Event
from core.reactor import ReactorThread
from rfid.rfid import RfidThread


def main():
	log.loglevel = log.LVL_DBG

	context = Context()

	# todo delete
	from core.user import User
	giulio = User()
	giulio.name = "Giulio"
	giulio.tag = 797313096147
	giulio.glass.capacity = 250
	giulio.glass.weight = 280
	evt = Event(Event.REGISTRATION_REQUESTED)
	evt.user = giulio
	context.queue.put(evt)

	core_th = ReactorThread(context)
	rfid_th = RfidThread(context.queue)
	# gui_th = GuiThread(context.queue)

	try:
		core_th.start()
		rfid_th.start()
		# gui_th.start()

		rfid_th.join()
		core_th.join()

	except KeyboardInterrupt:
		evt = Event(Event.SIGINT)
		context.queue.put(evt)

		rfid_th.running = False
	# gui_th.running = False

	# gui_th.join()
	core_th.join()
	rfid_th.join()
	GPIO.cleanup()


if __name__ == "__main__":
	main()
