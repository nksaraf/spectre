import re
import json

from constants import *
import utils
import services

class SpectreProtocolHandler():

    def __init__(self, server):
        self.server = server

    def handle(self, client, request):
        try:
            data = json.loads(request)
            self.server.log('{} [{}]: {}'.format(data["name"], data["action"].upper(), data["content"]), 'recv')
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
        return

    def _understand(self, client, data):
        if "weather" in data["content"]:
            weather = services.get_weather()
            self.respond(True, Action.REPLY, weather, client)
        appl = ["light", "fan"]
        for appli in appl:
            if appli in data["content"]:
                if "on" in data["content"]:
                    action = "on"
                else:
                    action = "off"
                worlds = self.server.get_clients("env")
                if len(worlds) == 0:
                    self.respond(False, Action.REPLY, "Sorry. Couldnt find the {}s".format(appli), client, "world not connected")
                    return
                content = {
                    "object": appli,
                    "action": action
                }
                self.respond(True, Action.REPLY, "Switching {}s {}".format(appli, action), client)
                for world in worlds:
                    self.respond(True, Action.COMMAND, content, world)

    def respond(self, success, action, reply, client, error='', request=None):
        response = {}
        response["action"] = action
        response["for"] = client["name"]
        response["name"] = self.server.obj["name"]
        response["content"] = reply
        if success:
            response["status"] = 'OK'
            self.server.log('spectre -> {} [{}]: {}'.format(client["name"], action.upper(), reply), 'sent')
        else:
            response["status"] = "ERROR"
            response["error"] = error
            self.server.log('spectre -> {} [{}]: {}'.format(client["name"], "ERROR", reply), 'sent')
        to_send = json.dumps(response)
        client["write_queue"].put(bytes(utils.proto_string(to_send), 'utf-8'))

    def _respond(self, client, response):
        pass

class ProtocolError(Exception):

    def __init__(self, request, error, message):
        self.request = request
        self.error = error
        self.message = message

    def __str__(self):
        return 'ProtocolError: {} on request "{}"'.format(self.error, self.request)



