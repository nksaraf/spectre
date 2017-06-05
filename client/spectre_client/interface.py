import RPIO as GPIO
from constants import *

class Interface():
    pass

class SimpleAppliance(Interface):

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(True)
        GPIO.setup(G_LIGHT, GPIO.OUT)
        GPIO.setup(G_FAN, GPIO.OUT)
        GPIO.output(G_LIGHT, GPIO.LOW)
        GPIO.output(G_FAN, GPIO.LOW)

    def handle(self, command):
        pass


class Music(Interface):

    def handle(self, command):
        pass