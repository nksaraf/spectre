import sys
import socket
import select
import json

from spectre_client.constants import *
from spectre_client import utils

class Client():

    def __init__(self, name, address):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.connect(address)
        self.name = name
        self.properties = {}
        self.properties["name"] = name
     
    def run(self):
        raise NotImplementedError()

    def get_data(self):
        length = None
        buf = ""
        while True:
            data = self.socket.recv(BUF_SIZE)
            if not data:
                sys.exit()
            buf += str(data, 'utf-8')
            while True:
                if length is None:
                    if '#' not in buf:
                        break
                    length_str, ign, buf = buf.partition('#')
                    length = int(length_str)

                if len(buf) < length:
                    break
                return json.loads(buf[:length])

    def send_data(self, action, data):
        to_send = {}
        to_send["action"] = action
        to_send["content"] = data
        to_send = {**to_send, **self.properties}
        self.socket.send(bytes(utils.proto_string(json.dumps(to_send)), 'utf-8'))

if __name__ == '__main__':
    try:
        client = Client('nikhil', ADDRESS)
        client.run()
    except (KeyboardInterrupt, SystemExit):
        client.socket.close()
        sys.exit(0)