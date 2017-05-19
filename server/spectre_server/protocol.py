import re
import json

from .constants import *
from . import utils
from . import services

class ProtocolHandler():

    def __init__(self, server):
        self.server = server

    def handle(self, client, request):
        try:
            data = json.loads(request)
            if data is None:
                raise ProtocolError(request, 'Not json format', 'Fuck off')
            if data["action"] == ClientAction.ID:
                self._identify(client, data)
            elif data["action"] == ClientAction.TALK:
                self._understand(client, data)
            else:
                raise ProtocolError(request, 'Action not supported', 'Bad luck')
        except ProtocolError as e:
            self.server.log("{}: {}".format('Protocol Error', e.error), 'error')
            self._response(False, Action.COMPLAIN, e.message, client)

    def _identify(self, client, data):
        client["name"] = data["name"]
        client["sub-role"] = data["type"]
        self.respond(True, Action.ID, 'Hi, I am Spectre.', client)

    def _understand(self, client, data):
        if "weather" in data["content"]:
            weather = services.get_weather()
            self.respond(True, Action.REPLY, weather, client)
        

#         request = Request(request)
#         if request.error is None:
#             if not client.authorized and OP_ID in request.tags:
#                 response = ProtocolHandler.authorize(client, request) 
#             elif client.authorized:
#                 response = ProtocolHandler.set_response(True, 'All good!', request=request)
#             else:
#                 response = ProtocolHandler.set_response(False, 'Who are you?', 'unauthorized', request=request)
#         else:
#             response = ProtocolHandler.set_response(False, 'Something is wrong', 'protocol error', request=request)
#         return response

#     @staticmethod
#     def authorize(client, request):
#         response = ProtocolHandler.set_response(True, 'Hi, I am {}. Nice to meet you.'.format(NAME), request=request)
#         client.nickname = request.body
#         client.authorized = True
#         return response

    def respond(self, success, action, reply, client, error='', request=None):
        response = {}
        response["action"] = action
        response["for"] = client["name"]
        response["name"] = self.server.obj["name"]
        if success:
            response["status"] = 'OK'
        else:
            response["status"] = "ERROR"
            response["error"] = error
        response["reply"] = reply
        to_send = json.dumps(response)
        self.server.log('Sending to {}: {}'.format(client["name"], to_send), 'sent')
        client["write_queue"].put(bytes(utils.proto_string(to_send), 'utf-8'))

    def _respond(self, client, response):
        pass

# class Request():
#     def __init__(self, request):
#         self.request = request
#         try:
#             self.parse_request(request)
#             self.error = None
#         except ProtocolError as e:
#             self.protocol = ''
#             self.body = ''
#             self.tags = []
#             self.error = e

#     def parse_request(self, request):
#         parsed = re.search(REQUEST_REGEX, request)
#         if parsed is None:
#             raise ProtocolError(request, 'error', 'msg')
#         parts = parsed.groupdict()
#         self.protocol = parts["proto"]
#         self.body = parts["body"]
#         self.tags = []
#         tags = re.findall(TAGS_REGEX, parts["tags"])
#         for tag in tags:
#             if tag[0] == '':
#                 self.tags.append((tag[1], tag[2]))
#             else:
#                 self.tags.append(tag[0])


class ProtocolError(Exception):

    def __init__(self, request, error, message):
        self.request = request
        self.error = error
        self.message = message

    def __str__(self):
        return 'ProtocolError: {} on request "{}"'.format(self.error, self.request)



