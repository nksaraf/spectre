NAME = 'spectre'

DEFAULT_IP = '192.168.1.69'
DEFAULT_ME = 'nikhil'
PORT = 6969
ADDRESS = (DEFAULT_IP, PORT)
BUF_SIZE = 1024
PROTOCOL = '{}://'.format(NAME)
MOPIDY_IP = '192.168.1.69'

GEO_API = 'http://freegeoip.net/json'

MY_MESSENGER_ID = '1748668891827074'
FB_ACCESS_TOKEN = "EAAJTxhZBMgZAYBABn4IrV9Dh1ZBa23ezOF3lV6NVJDpV6SSZA5LIWN1ySzGYvqZAvsAmaXfHIUmQEIaJjG8YsOD5nXWRvgZAAIQoHRA7U2fU60FuRZCk3oLEIuYrhjVCPdfl8qHhN5M6O59Pz3zGZCyCZBxblKLFhKsyxH8YIOUa1WwZDZD"
FB_GRAPH_ENDPOINT = "https://graph.facebook.com/v2.6/me/messages?access_token=" + FB_ACCESS_TOKEN

class Action():	
	ID = 'id'
	TALK = 'talk'

class ServerAction():
	ID = 'id'
	REPLY = 'reply'
	COMMAND = 'cmd'
	GET = 'get'
	COMPLAIN = 'complain'

G_LIGHT = 14
G_FAN = 15