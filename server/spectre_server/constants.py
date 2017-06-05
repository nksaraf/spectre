NAME = 'spectre'

IP = '192.168.1.69'
PORT = 6969
TIMEOUT = 1000
ADDRESS = (IP, PORT)
BUF_SIZE = 1024
PROTOCOL = '{}://'.format(NAME)
MOPIDY_IP = '192.168.1.69'

class ClientAction():
	ID = 'id'
	TALK = 'talk'

class Action():
	ID = 'id'
	REPLY = 'reply'
	COMMAND = 'cmd'
	GET = 'get'
	COMPLAIN = 'complain'

REQUEST_REGEX = r'^(?P<proto>spectre://)(?P<tags>(?:\[[a-z]+\]|\[[a-z]+:[^\[:\]]+\])*)(?P<body>.+)$'
TAGS_REGEX = r'\[([a-z]+)\]|\[([a-z]+):([^\[:\]]+)\]'

WEATHER_APP_ID = 'c0d3d8b07d428c174ecd945a1f35ea7b'
WEATHER_ENDPOINT = 'http://api.openweathermap.org/data/2.5/weather?appid={}&lat={}&lon={}'
GEO_API = 'http://freegeoip.net/json'