import requests
import json
from .constants import *

def get_location():
	location = requests.get(GEO_API)
	if location.status_code == 200:
		return True, location.json()
	else:
		return False, None

def proto_string(msg):
	msg = msg.strip()
	return '{}#{}'.format(int(len(msg)), msg)