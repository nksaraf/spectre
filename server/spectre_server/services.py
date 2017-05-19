import requests
import json

from spectre_server.constants import *

def get_location():
	location = requests.get(GEO_API)
	if location.status_code == 200:
		return True, location.json()
	else:
		return False, None

def get_weather():
	no_error, loc = get_location()
	if no_error:
		weather = requests.get(WEATHER_ENDPOINT.format(WEATHER_APP_ID, loc["latitude"], loc["longitude"])).json()
		if weather["cod"] == 200:
			return weather["weather"][0]["description"]
	return 'Couldnt get weather info'