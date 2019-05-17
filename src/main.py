#!/usr/bin/python3
import argparse

from core.context import Context
from core.core import Core

parser = argparse.ArgumentParser()
parser.add_argument("port", help="port to bind to", type=int)
args = parser.parse_args()


def main():
	# start
	# - core thread
	# - gui thread
	# - rfid thread

	context = Context(args)
	loop = Core(context)
	return loop.run()


if __name__ == "__main__":
	main()
