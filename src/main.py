#!/usr/bin/python3
import sys

from core.core import Mainloop


def main():
    loop = Mainloop()
    return loop.run(sys.argv)


if __name__ == "__main__":
    main()
