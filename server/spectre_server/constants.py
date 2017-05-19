NAME = 'spectre'

IP = '10.147.9.149'
PORT = 6969
TIMEOUT = 1000
ADDRESS = (IP, PORT)
BUF_SIZE = 4096
PROTOCOL = '{}://'.format(NAME)

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