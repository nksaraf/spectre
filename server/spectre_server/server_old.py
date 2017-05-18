import sys
import socket
import threading
import time
import json

from spectre_server import protocol
from spectre_server import utils
from spectre_server.constants import *

class Server(threading.Thread):

    def __init__(self, address):
        threading.Thread.__init__(self)
        self.address = address
        ip, port = address
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(self.address)
        print("[+] Server started at {}:{}".format(ip, port))
        self.clients = [self.server]
        

    def run(self):
        while True:
            self.server.listen(4) 
            print("[+] Waiting for connections from clients...") 
            (conn, (ip,port)) = self.server.accept() 
            newthread = ClientThread(conn, ip, port, self)
            newthread.setDaemon(True)
            newthread.start()
            self.threads.append(newthread)
        for thread in threads:
            thread.join()
        self.server.close()

    def test(self):
        print('It worked!')


class ClientThread(threading.Thread):

    def __init__(self, conn, ip, port, server): 
        threading.Thread.__init__(self)
        self.conn = conn
        self.ip = ip 
        self.port = port 
        self.server = server
        self.request = ""
        self.authorized = False
        self.nickname = 'unauthorized'
        print("[+] New server socket thread started for " + ip + ":" + str(port))
 
    def run(self): 
        while True:
            length = None
            buf = "" #buffer
            while True:
                data = self.conn.recv(BUF_SIZE)
                if not data:
                    break
                buf += str(data, 'utf-8')
                while True:
                    if length is None:
                        if '#' not in buf:
                            break
                        length_str, ign, buf = buf.partition('#')
                        try:
                            length = int(length_str)
                        except ValueError:
                            print('ProtocolError')

                    if len(buf) < length:
                        break
                    request = buf[:length]
                    buf = buf[length:]
                    length = None
                    response = self.handle_request(request)

        self.conn.close()
        self.join()

    def handle_request(self, request):
        self.server.test()
        print("[*] Request from {}: {}".format('{}: {}'.format(self.nickname,self.conn.getsockname()), request))
        response = protocol.ProtocolHandler.handle(self, request)
        self.conn.send(bytes(utils.proto_string(json.dumps(response)), 'utf-8'))
        print("[+] Response {}- {}".format(response["status"], response["reply"]))
        return response


if __name__ == '__main__':
    try:
        server = Server(ADDRESS)
        server.setDaemon(True)
        server.start()
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        server.server.close()
        sys.exit(0)