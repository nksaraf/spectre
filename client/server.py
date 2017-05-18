from flask import Flask, request
import requests
import select
import threading

from spectre_client import messenger
 
class SpectreConnection(threading.Thread):
    def __init__(self, name, address):
        threading.Thread.__init__(self)
        try:
            self.client = messenger.MessengerClient(name, address)
        except ConnectionRefusedError:
            print("blah")

    def is_writable(self):
        if select.select([], [self.client.socket], [], 0) == ([], [self.client.socket], []):
            return True
        else:
            return False

    def read_data(self):
        if select.select([self.client.socket], [], [], 0) == ([self.client.socket], [], []):
            data = self.client.get_data()

    def run(self):
        while True:
            read, _, _ = select.select([self.client.socket], [], [], 1)
            if read:
                data = self.client.get_data()
                reply('1748668891827074', data)


spectre = SpectreConnection('nikhil', ('localhost', 6969))

app = Flask(__name__)
ACCESS_TOKEN = "EAAJTxhZBMgZAYBABn4IrV9Dh1ZBa23ezOF3lV6NVJDpV6SSZA5LIWN1ySzGYvqZAvsAmaXfHIUmQEIaJjG8YsOD5nXWRvgZAAIQoHRA7U2fU60FuRZCk3oLEIuYrhjVCPdfl8qHhN5M6O59Pz3zGZCyCZBxblKLFhKsyxH8YIOUa1WwZDZD"
def reply(user_id, msg):
    data = {
        "recipient": {"id": user_id},
        "message": {"text": msg}
    }
    resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=data)
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
    if not spectre.is_writable():
        data = spectre.read_data()
        if data:
            reply(sender, data)
    response = spectre.client.run(message)
    print(response)
    reply(sender, response)
    return "ok"
 
if __name__ == '__main__':
    spectre.start()
    app.run(debug=True, use_reloader=False)