import socket
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("port", help="port to bind to", type=int)


class Context:
    def __init__(self):
        self.args = parser.parse_args()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("0.0.0.0", self.args.port))
        self.valid = True
