import sys
import socket

from spectre_client.constants import *
from spectre_client import utils
from spectre_client import client

class MessengerClient(client.Client):

    def __init__(self, name, address):
        client.Client.__init__(self, name, address)
    
    def run(self, message):
        self.send_data(message)
        data = self.get_data()
        return data

if __name__ == '__main__':
    try:
        client = MessengerClient('nikhil', ADDRESS)
        client.run()
    except (KeyboardInterrupt, SystemExit):
        client.socket.close()
        sys.exit(0)