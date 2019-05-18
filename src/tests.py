#!/usr/bin/python3
import argparse
import sys
import threading
import time
from queue import Queue

from core import log
from core.context import Context
from core.events import Event, Handlers
from core.reactor import Reactor
from core.water_machine import WaterMachine
from gui.gui import TextGui
from rfid.rfid import RFID
from scale.scale import FakeScale, Scale


class Object(object):
	pass


args = Object()
args.port = 5555

log.loglevel = log.LVL_DBG

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
		consumer = Reactor(context)
		consumer.add_handler(Event.RFID_DETECTED, Handlers.rfid_detected)
		context.scale = FakeScale()
		context.gui = TextGui()
		self.retcode = consumer.run()
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


def core_test():
	main_t = MainThread()
	main_t.set_queue(main_queue)
	main_t.start()

	send_invalid(main_queue)
	assert (context.state_machine.state == WaterMachine.State.UNINIT)

	send_wrong_type(main_queue)
	assert (context.state_machine.state == WaterMachine.State.UNINIT)

	send_rfid("ifoifjo23iofj", main_queue)
	assert (context.state_machine.state == WaterMachine.State.UNINIT)

	context.state_machine.initialize()
	send_rfid("ifoifjo23iofj", main_queue)
	assert (timeout(0.01, context.state_machine.state, WaterMachine.State.GLASS_ON))

	send_killevt(main_queue)
	main_t.join()
	assert (main_t.retcode == 0)


def scale_test():
	log.ok("testing scale..")
	scale = Scale()
	for i in range(10):
		w = scale.get_weight()
		log.ok("weight = " + str(w))
		assert w is not None


def rfid_test():
	log.ok("testing rfid [timeout in 10s!]")
	rfid = RFID()
	ok, tag = rfid.read_id()
	log.yay("read tag " + str(tag))
	timeout(10, ok, True)
	pass


def relay_test():
	log.ok("testing relay..")


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--scale', help='perform scale test', action='store_true')
	parser.add_argument('--rfid', help='perform rfid test', action='store_true')
	parser.add_argument('--relay', help='perform relay board test', action='store_true')
	parser.add_argument('--allio', help='perform all sensors/io tests', action='store_true')
	parser.add_argument('--all', help='perform all tests', action='store_true')
	parser.add_argument('--core', help='perform core test', action='store_true')

	args = parser.parse_args()
	if len(sys.argv) == 1:
		args.all = True

	if args.scale or args.all or args.allio:
		scale_test()
	if args.rfid or args.all or args.allio:
		rfid_test()
	if args.relay or args.all or args.allio:
		relay_test()
	if args.core or args.all:
		core_test()

	log.yay(">>>>>>>>>>> All good <<<<<<<<<<<<")
