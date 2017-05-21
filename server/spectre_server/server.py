import sys
import socket
import select
import queue
import blessings

from constants import *
import utils
import protocol

READ_ONLY = select.POLLIN | select.POLLPRI | select.POLLHUP | select.POLLERR
READ_WRITE = READ_ONLY | select.POLLOUT
term = blessings.Terminal()

class Spectre():

    def __init__(self):
        self.address = ADDRESS
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(self.address)
        server.listen(5)
        self.handler = protocol.SpectreProtocolHandler(self)
        self.log('Serving at {}:{}'.format(IP, PORT), 'config')
        self.obj = self.socket_obj(server, False)
        self.socket_map = {
            server.fileno(): self.obj,
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
                    if client["role"] == 'server':
                        self.new_client()
                    else:
                        data = self.get_data(client)
                        if data is not None:
                            self.handler.handle(client, data)
                elif flag & (select.POLLHUP | select.POLLERR):
                    self.close_connection(client)
                elif flag & select.POLLOUT:
                    # Socket is ready to send data, if there is any to send.
                    try:
                        to_send = client["write_queue"].get_nowait()
                    except queue.Empty:
                        pass
                    else:
                        client["socket"].send(to_send)
                else:
                    pass

    def get_data(self, client):
        length = None
        buf = ""
        while True:
            data = client["socket"].recv(BUF_SIZE)
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
        self.log('New connection made at {}'.format(address), 'new_client')

    def close_connection(self, client):
        self.log('Closing connection with {}'.format(client["name"]), 'closing')
        self.poller.unregister(client["socket"])
        self.socket_map[client["socket"].fileno()] = None
        client["socket"].close()

    def socket_obj(self, socket, client=True):
        if client:
            obj = {
                "name": socket.getpeername(),
                "role": "client",
                "sub-role": "client",
                "socket": socket,
                "write_queue": queue.Queue()
            }
        else:
            obj = {
                "name": "spectre",
                "role": "server",
                "socket": socket,
            }
        return obj

    def handle(self, client, data):
        for key, value in self.socket_map.items():
            if not (value is None or value["role"] == 'server'):
                self.log('Sending to {}: {}'.format(value["socket"].getpeername(), data), 'sent')
                value["write_queue"].put('{} said {}'.format(client["socket"].getpeername(), data))

    def log(self, message, category):
        if category == 'config':
            print('[+] {}'.format(message))
        elif category == 'new_client':
            print(term.green('[+] {}'.format(message)))
        elif category == 'recv':
            print(term.magenta('[+] {}'.format(message)))
        elif category == 'sent':
            print(term.blue('[+] {}'.format(message)))
        elif category == 'closing':
            print(term.red('[+] {}'.format(message)))
        else:
            print('[+] {}'.format(message))

    def get_client(self, role):
        relevant = []
        for key, client in self.socket_map.items():
            if not client is None and client["role"] == "client" and client["sub-role"] == role:
                relevant.append(client)
        return relevant

if __name__ == '__main__':
    try:
        spectre = Spectre()
        spectre.serve()
    except (KeyboardInterrupt, SystemExit):
        spectre.server.close()
        sys.exit(0)