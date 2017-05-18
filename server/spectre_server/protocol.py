import re
import json

from spectre_server import speech
from spectre_server.constants import *

class ProtocolHandler():

    @staticmethod
    def handle(client, request):
        request = Request(request)
        if request.error is None:
            if not client.authorized and OP_ID in request.tags:
                response = ProtocolHandler.authorize(client, request) 
            elif client.authorized:
                response = ProtocolHandler.set_response(True, 'All good!', request=request)
            else:
                response = ProtocolHandler.set_response(False, 'Who are you?', 'unauthorized', request=request)
        else:
            response = ProtocolHandler.set_response(False, 'Something is wrong', 'protocol error', request=request)
        return response

    @staticmethod
    def authorize(client, request):
        response = ProtocolHandler.set_response(True, 'Hi, I am {}. Nice to meet you.'.format(NAME), request=request)
        client.nickname = request.body
        client.authorized = True
        return response

    @staticmethod
    def set_response(success, reply, error='', request=None):
        response = {}
        if success:
            response["status"] = 'OK'
        else:
            response["status"] = "ERROR"
            response["error"] = error
        response["reply"] = reply
        if request is not None and 'speak' in request.tags:
            response["audio"] = speech.audio(reply)
        return response

class Request():
    def __init__(self, request):
        self.request = request
        try:
            self.parse_request(request)
            self.error = None
        except ProtocolError as e:
            self.protocol = ''
            self.body = ''
            self.tags = []
            self.error = e

    def parse_request(self, request):
        parsed = re.search(REQUEST_REGEX, request)
        if parsed is None:
            raise ProtocolError(request, 'error', 'msg')
        parts = parsed.groupdict()
        self.protocol = parts["proto"]
        self.body = parts["body"]
        self.tags = []
        tags = re.findall(TAGS_REGEX, parts["tags"])
        for tag in tags:
            if tag[0] == '':
                self.tags.append((tag[1], tag[2]))
            else:
                self.tags.append(tag[0])


class ProtocolError(Exception):

    def __init__(self, request, error, message):
        self.request = request
        self.error = error
        self.message = message

    def __str__(self):
        return 'ProtocolError: {} on request "{}"'.format(self.error, self.request)



