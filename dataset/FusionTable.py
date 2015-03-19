__author__ = 'Jakub Dubec'
from config import config
import requests
from auth.GoogleAuth import auth
from datetime import datetime


class FusionTable:
	def __init__(self):
		print("[FusionTable] Initialization")

	@staticmethod
	def insert(data):
		add_record = "INSERT INTO {0} (Time, Temperature, Humidity) VALUES ('{1}', '{2}', '{3}')".format(config.get("Data", "table"), datetime.now().isoformat(' '), str(data[0]), str(data[1]))
		payload = {"sql": add_record}
		headers = {"Authorization": "Bearer " + auth.get_access_token()}
		r = requests.post("https://www.googleapis.com/fusiontables/v2/query", payload, headers=headers)
		response = r.json()
		if 'error' in response:
			print "[FusionTable] Error response from Google server: " + response['error']['message']
			return False
		else:
			print("[FusionTable] Record has been successfully inserted!")
			return True