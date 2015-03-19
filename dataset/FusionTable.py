__author__ = 'Jakub Dubec'
from config import config
import requests
from auth.GoogleAuth import auth
from datetime import datetime
from pprint import pprint


class FusionTable:
	def __init__(self):
		print("[FusionTable] Initialization")

	@staticmethod
	def insert(data):
		add_record = "INSERT INTO {0} (Time, Temperature, Humidity) VALUES ('{1}', '{2}', '{3}')".format(config.get("Data", "table"), datetime.now().isoformat(' '), str(data[0]), str(data[1]))
		payload = {"sql": add_record, "access_token": auth.get_access_token()}
		headers = {"Authorization": "Bearer " + auth.get_access_token()}
		pprint(payload)
		r = requests.post("https://www.googleapis.com/fusiontables/v2/query", payload, headers=headers)
		response = r.json()
		if 'error' in response:
			print "[FusionTable] Error response from Google server: " + response['error']['message']
			pprint(response)
			return False
		else:
			print("[FusionTable] Record has been successfully inserted!")
			return True