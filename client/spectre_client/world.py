import sys
import socket
import RPIO as GPIO

from constants import *
import client
import error
import interface

class WorldClient(client.Client):
    def __init__(self, address):
        world = World()
        client.Client.__init__(self, "world", "env", address, world)
        self.properties["os"] = sys.platform

    def run(self):
        while True:
            try:
                data = self.get_data()
            except error.ConnectionClosedError:
                sys.exit(0)
            self.handler.handle(data)


class World(object):

    def __init__(self):
        simple_appliance = interface.SimpleAppliance()
        music = interface.Music()

    def handle(self, data):
        if data["action"] == ServerAction.COMMAND:
            if data["content"]["object"] == "light":
                if data["content"]["action"] == "on":
                    print("lights on")
                    GPIO.output(G_LIGHT, GPIO.HIGH)
                elif data["content"]["action"] == "off":
                    print("lights off")
                    GPIO.output(G_LIGHT, GPIO.LOW)
            if data["content"]["object"] == "fan":
                if data["content"]["action"] == "on":
                    GPIO.output(G_FAN, GPIO.HIGH)
                elif data["content"]["action"] == "off":
                    GPIO.output(G_FAN, GPIO.LOW)

if __name__ == '__main__':
    address = ADDRESS
    if len(sys.argv) > 1:
        address = (sys.argv[1], PORT)
    try:
        client = WorldClient(address)
        client.run()
    except (KeyboardInterrupt, SystemExit):
        client.socket.close()
        GPIO.cleanup()
        sys.exit(0)