import requests
import json
from constants import *
try:
	from mopidy.models import serialize
except ModuleNotFoundError:
	pass

def get_location():
	location = requests.get(GEO_API)
	if location.status_code == 200:
		return True, location.json()
	else:
		return False, None

def proto_string(msg):
	msg = msg.strip()
	return '{}#{}'.format(int(len(msg)), msg)

def mopidy_request(method, params):
	data = {
		"jsonrpc": "2.0",
		"id": 1,
		"method": method,
		"params": params
	}
	response = requests.post("http://{}:6680/mopidy/rpc".format(MOPIDY_IP), data=json.dumps(data, cls=serialize.ModelJSONEncoder))
	response = json.loads(response.content, object_hook=serialize.model_json_decoder)
	return response["result"]

