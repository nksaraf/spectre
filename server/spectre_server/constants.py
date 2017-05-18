NAME = 'spectre'

IP = 'localhost'
PORT = 6969
TIMEOUT = 1000

ADDRESS = (IP, PORT)
BUF_SIZE = 4096

PROTOCOL = '{}://'.format(NAME)

OP_ID = 'iam'
OP_GET = 'get'
OP_RESPOND = 'respond'

REQUEST_REGEX = r'^(?P<proto>spectre://)(?P<tags>(?:\[[a-z]+\]|\[[a-z]+:[^\[:\]]+\])*)(?P<body>.+)$'
TAGS_REGEX = r'\[([a-z]+)\]|\[([a-z]+):([^\[:\]]+)\]'

WEATHER_API = 'GyYwxJiPof5jT6OVQCOyoCAMUn4v3lYjWMWyWNkNtr4a'
WEATHER_ENDPOINT = 'http://api.openweathermap.org/data/2.5/weather?appid={}&q={},{}'