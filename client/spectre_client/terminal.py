import sys
import socket
import select
import time
import blessings

from constants import *
import client
import utils
import error

term = blessings.Terminal()
class TerminalClient(client.Client):

    def __init__(self, name, address):
        client.Client.__init__(self, name, "user", address, None)
        self.properties["os"] = sys.platform
  
    def run(self):
        while True:
            sys.stdout.write('> '); sys.stdout.flush()
            socks = [sys.stdin, self.socket]
            readable, _, _ = select.select(socks, [], [])
            for conn in readable:
                if conn == self.socket:
                    try:
                        data = self.get_data()
                        if data["action"] == ServerAction.REPLY:
                            print(term.green('{}: [{}] {}'.format(data["name"], data["status"], data["content"]))
                    except error.ConnectionClosedError:
                        sys.exit()
                else:
                    data = sys.stdin.readline()
                    self.send_data(Action.TALK, data.strip())

if __name__ == '__main__':
    try:
        client = TerminalClient('nikhil', ADDRESS)
        client.run()
    except (KeyboardInterrupt, SystemExit):
        client.socket.close()
        sys.exit(0)