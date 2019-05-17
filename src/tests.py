#!/usr/bin/python3
import threading
from queue import Queue

import time

from core import handlers
from core import log
from core.context import Context
from core.evtconsumer import EvtConsumer
from core.event import Event
from core.state_machine import StateMachine


class Object(object):
	pass


args = Object()
args.port = 5555

log.loglevel = log.LVL_OK

# globally expose internals
main_queue = Queue()
context = Context(args)


class MainThread(threading.Thread):
	def __init__(self):
		self.queue = None
		self.retcode = None
		super().__init__()

	def set_queue(self, queue):
		self.queue = queue

	def run(self):
		context.queue = self.queue
		loop = EvtConsumer(context)
		loop.add_handler(Event.RFID_DETECTED, handlers.rfid_detected)
		self.retcode = loop.run()
		return


def qpush(evt):
	main_queue.put(evt)
	time.sleep(0.001)


def send_json_msg(msg, queue):
	evt = Event()
	evt.data = str.encode(msg)
	evt.type = Event.JSON
	qpush(evt)


def send_rfid(rfid, queue):
	evt = Event()
	evt.type = Event.RFID_DETECTED
	evt.rfid = rfid
	qpush(evt)


def send_killevt(queue):
	evt = Event()
	evt.type = Event.SIGINT
	qpush(evt)


def send_invalid(queue):
	evt = Event()
	evt.type = "what is this?"
	qpush(evt)


def send_wrong_type(queue):
	evt = "not an event"
	qpush(evt)


def timeout(tout, a, b):
	start = time.time()
	while time.time() - start < tout:
		if a == b:
			return True
		time.sleep(0.000001)
	return False


def main():
	main_t = MainThread()
	main_t.set_queue(main_queue)
	main_t.start()
	log.ok("started main thread")

	send_invalid(main_queue)
	assert (context.state_machine.state == StateMachine.State.UNINIT)

	send_wrong_type(main_queue)
	assert (context.state_machine.state == StateMachine.State.UNINIT)

	send_rfid("ifoifjo23iofj", main_queue)
	assert (context.state_machine.state == StateMachine.State.UNINIT)

	context.state_machine.initialize()
	send_rfid("ifoifjo23iofj", main_queue)
	assert(timeout(0.01, context.state_machine.state, StateMachine.State.GLASS_ON))

	log.ok("killing main thread")
	send_killevt(main_queue)

	main_t.join()
	assert (main_t.retcode == 0)


if __name__ == "__main__":
	main()
