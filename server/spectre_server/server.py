import sys
import socket
import select
import queue

from spectre_server.constants import *
from spectre_server import utils

READ_ONLY = select.POLLIN | select.POLLPRI | select.POLLHUP | select.POLLERR
READ_WRITE = READ_ONLY | select.POLLOUT

class Spectre():

    def __init__(self):
        self.address = ADDRESS
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(self.address)
        server.listen(5)
        self.log('Serving at {}:{}'.format(IP, PORT))
        self.socket_map = {
            server.fileno(): self.socket_obj(server, False),
        }
        self.server = server
        self.poller = select.poll()
        self.poller.register(server, READ_ONLY)

    def serve(self):
        while True:
            events = self.poller.poll(TIMEOUT)
            for fd, flag in events:
                client = self.socket_map[fd]
                if flag & (select.POLLIN | select.POLLPRI):
                    if client["socket"] is self.server:
                        self.new_client()
                    else:
                        data = self.get_data(client["socket"])
                        if data is not None:
                            self.log('Received from {}: {}'.format(client["socket"].getpeername(), data))
                            self.handle(client, data)
                elif flag & (select.POLLHUP | select.POLLERR):
                    self.close_connection(client["socket"])
                elif flag & select.POLLOUT:
                    # Socket is ready to send data, if there is any to send.
                    try:
                        to_send = client["write_queue"].get_nowait()
                    except queue.Empty:
                        pass
                    else:
                        client["socket"].send(bytes(utils.proto_string(to_send), 'utf-8'))
                else:
                    pass

    def get_data(self, client):
        length = None
        buf = ""
        while True:
            data = client.recv(BUF_SIZE)
            if not data:
                self.close_connection(client)
                return None
            buf += str(data, 'utf-8')
            while True:
                if length is None:
                    if '#' not in buf:
                        break
                    length_str, ign, buf = buf.partition('#')
                    length = int(length_str)

                if len(buf) < length:
                    break
                return buf[:length]

    def new_client(self):
        socket, address = self.server.accept()
        self.socket_map[socket.fileno()] = self.socket_obj(socket)
        self.poller.register(socket, READ_WRITE)
        self.log('New connection made at {}'.format(address))

    def close_connection(self, client):
        self.poller.unregister(client)
        self.socket_map[client.fileno()] = None
        client.close()
        self.log('Closing connection..')

    def socket_obj(self, socket, client=True):
        if client:
            obj = {
                "name": "client",
                "socket": socket,
                "write_queue": queue.Queue()
            }
        else:
            obj = {
                "name": "server",
                "socket": socket,
            }
        return obj

    def handle(self, client, data):
        for key, value in self.socket_map.items():
            if not (value is None or value["name"] == 'server'):
                self.log('Sending to {}: {}'.format(value["socket"].getpeername(), data))
                value["write_queue"].put('{} said {}'.format(client["socket"].getpeername(), data))

    def log(self, message):
        print('[+] {}'.format(message))

if __name__ == '__main__':
    try:
        spectre = Spectre()
        spectre.serve()
    except (KeyboardInterrupt, SystemExit):
        spectre.server.close()
        sys.exit(0)