import sys
import socket
import select

from spectre_client.constants import *
from spectre_client import client

class TerminalClient(client.Client):

    def __init__(self, name, address):
        client.Client.__init__(self, name, address)
  
    def run(self):
        while True:
            sys.stdout.write('> '); sys.stdout.flush()
            socks = [sys.stdin, self.socket]
            readable, _, _ = select.select(socks, [], [])
            
            for conn in readable:
                if conn == self.socket:
                    data = self.get_data()
                    print(data)
                else:
                    data = sys.stdin.readline()
                    self.send_data(data)

if __name__ == '__main__':
    try:
        client = TerminalClient('nikhil', ADDRESS)
        client.run()
    except (KeyboardInterrupt, SystemExit):
        client.socket.close()
        sys.exit(0)