#!/usr/bin/python3
from core.context import Context
from core.core import Mainloop
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("port", help="port to bind to", type=int)
args = parser.parse_args()


def main():
    context = Context(args)
    loop = Mainloop(context)
    return loop.run()


if __name__ == "__main__":
    main()
