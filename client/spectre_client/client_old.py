import json
import sys
import socket
import select
import speech_recognition
import time
import threading

from spectre_client import protocol
from spectre_client import utils
from spectre_client.constants import *

class Client(threading.Thread):

    def __init__(self, name, address, speak=False):
        threading.Thread.__init__(self)
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect(address)
        self.name = name
        self.authorized = False
        self.request = ""
        self.response = {}
        self.tags = []
        self.speak = speak
        self.tags.append(('os', sys.platform))
        if speak:
            self.tags.append('speak')
        no_error, location = utils.get_location()
        if no_error:
            self.tags.append(('lat', location["latitude"]))
            self.tags.append(('long', location["longitude"]))
        
    def run(self):
        while True:
            if not self.authorized:
                self.authorize()
                continue
            request = self.get_request()
            self.send_request(self.tags + [OP_GET], request)
            self.response = self.get_response()
            protocol.ClientProtocolHandler.handle_response(self, self.response)
            print('[+] {}: {}'.format(NAME.upper(), self.response["reply"]))

    def get_request(self):
        request = ''
        if self.speak:
            r = sr.Recognizer()
            while True:
                with sr.Microphone() as source:
                    try:
                        audio = r.listen(source, 5)
                        request = r.recognize_google(audio)
                    except Exception:
                        request = ''
                        writ, _, _ = select.select([sys.stdin], [], [], 1)
                        if writ:
                            request = sys.stdin.readline()
                    finally:
                        if len(request) > 0:
                            print('[*] {}: {}'.format(self.name.upper(), request))
                            break
        else:
            request = input('[*] {}: '.format(self.name.upper()))
        return request

    def send_request(self, tags, body):
        op = ''
        for tag in tags:
            if type(tag) == tuple:
                op += '[{}:{}]'.format(tag[0], tag[1])
            else:
                op += '[{}]'.format(tag)

        self.request = utils.proto_string(PROTOCOL + op + body)
        self.conn.send(bytes(self.request.strip(), 'utf-8'))

    def authorize(self):
        self.send_request(self.tags + [OP_ID], self.name)
        self.response = self.get_response()
        print('[+] {}: {}'.format(NAME.upper(), self.response["reply"]))
        if self.response["status"] != 'OK':
            return
        protocol.ClientProtocolHandler.handle_response(self, self.response)
        self.authorized = True

    def get_response(self):
        length = None
        buf = ""
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
                    length = int(length_str)

                if len(buf) < length:
                    break
                return json.loads(buf[:length])

if __name__ == '__main__':
    try:
        client = Client('nikhil', ADDRESS)
        client.setDaemon(True)
        client.start()
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        client.conn.close()
        sys.exit(0)
