#!/usr/bin/python3
import sys
from core.context import Context
from core.core import Mainloop


def main():
    context = Context()
    loop = Mainloop(context)
    return loop.run(sys.argv)


if __name__ == "__main__":
    main()
