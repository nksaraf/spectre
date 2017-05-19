from flask import Flask, request
import requests
import select
import threading
import sys
import socket

from constants import *
import utils
import client

class MessengerClient(client.Client):

    def __init__(self, name, address):
        client.Client.__init__(self, name, address)

    def is_writable(self):
        if select.select([], [self.socket], [], 0) == ([], [self.socket], []):
            return True
        else:
            return False

    def read_data(self):
        if select.select([self.socket], [], [], 0) == ([self.socket], [], []):
            data = self.get_data()
    
    def run(self, message):
        self.send_data(message)
        data = self.get_data()
        return data
 
class SpectreConnection(threading.Thread):
    def __init__(self, name, address):
        threading.Thread.__init__(self)
        try:
            self.client = messenger.MessengerClient(name, address)
        except ConnectionRefusedError:
            print("blah")

    def run(self):
        while True:
            read, _, _ = select.select([self.client.socket], [], [], 1)
            if read:
                data = self.client.get_data()
                reply(MY_MESSENGER_ID, data)


spectre = SpectreConnection('nikhil', ('localhost', 6969))
app = Flask(__name__)

def reply(user_id, msg):
    data = {
        "recipient": {"id": user_id},
        "message": {"text": msg}
    }
    resp = requests.post(FB_GRAPH_ENDPOINT, json=data)
    print(resp.content)
 
@app.route('/', methods=['GET'])
def handle_verification():
    print(request.args['hub.challenge'])
    return request.args['hub.challenge']

@app.route('/', methods=['POST'])
def handle_incoming_messages():
    data = request.json
    sender = data['entry'][0]['messaging'][0]['sender']['id']
    message = data['entry'][0]['messaging'][0]['message']['text']
    if not spectre.client.is_writable():
        data = spectre.client.read_data()
        if data:
            reply(sender, data)
    response = spectre.client.run(message)
    print(response)
    reply(sender, response)
    return "ok"
 
if __name__ == '__main__':
    spectre.start()
    app.run(debug=True, use_reloader=False)