#!/usr/bin/python3
import threading
from queue import Queue

from core import handlers
from core import log
from core.context import Context
from core.core import Core
from core.event import Event


class Object(object):
	pass


args = Object()
args.port = 5555

log.loglevel = log.LVL_OK
main_queue = Queue()


class MainThread(threading.Thread):
	def __init__(self):
		self.queue = None
		self.retcode = None
		super().__init__()

	def set_queue(self, queue):
		self.queue = queue

	def run(self):
		context = Context(args)
		context.queue = self.queue
		loop = Core(context)
		loop.add_handler(Event.RFID_DETECTED, handlers.rfid_detected)
		self.retcode = loop.run()
		return


def send_json_msg(msg, queue):
	evt = Event()
	evt.data = str.encode(msg)
	evt.type = Event.JSON
	queue.put_nowait(evt)


def send_rfid(rfid, queue):
	evt = Event()
	evt.type = Event.RFID_DETECTED
	evt.rfid = rfid
	queue.put_nowait(evt)


def send_killevt(queue):
	evt = Event()
	evt.type = Event.SIGINT
	queue.put_nowait(evt)


def send_invalid(queue):
	evt = Event()
	evt.type = "what is this?"
	queue.put_nowait(evt)


def send_wrong_type(queue):
	evt = "not an event"
	queue.put_nowait(evt)


def main():
	main_t = MainThread()
	main_t.set_queue(main_queue)
	main_t.start()
	log.ok("started main thread")

	send_rfid("ifoifjo23iofj", main_queue)
	send_invalid(main_queue)
	send_wrong_type(main_queue)

	log.ok("killing main thread")
	send_killevt(main_queue)

	main_t.join()
	assert (main_t.retcode == 0)


if __name__ == "__main__":
	main()
