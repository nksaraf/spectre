import sys
import socket
import select
import time

from spectre_client.constants import *
from spectre_client import client
from spectre_client import utils

class TerminalClient(client.Client):

    def __init__(self, name, address):
        client.Client.__init__(self, name, address)
        self.properties["os"] = sys.platform
        self.properties["type"] = "user"
  
    def run(self):
        while True:
            self.send_data(Action.ID, "")
            data = self.get_data()
            if data["action"] == ServerAction.ID and data["status"] == 'OK':
                print('{}: [{}] {}'.format(data["name"], data["status"], data["reply"]))
                break
            else:
                time.sleep(2)
        while True:
            sys.stdout.write('> '); sys.stdout.flush()
            socks = [sys.stdin, self.socket]
            readable, _, _ = select.select(socks, [], [])
            
            for conn in readable:
                if conn == self.socket:
                    data = self.get_data()
                    print('{}: [{}] {}'.format(data["name"], data["status"], data["reply"]))
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