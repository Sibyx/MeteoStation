__author__ = 'Jakub Dubec'
from config import config
import requests
from auth.GoogleAuth import auth
from datetime import datetime


class FusionTable:
	def __init__(self):
		print("[FusionTable] Inicializacia")

	@staticmethod
	def insert(data):
		print data[0]
		print data[1]
		add_record = "INSERT INTO {0} (Time, Temperature, Humidity) VALUES ('{1}', '{2}', '{3}')".format(config.get("Data", "table"), datetime.now().isoformat(' '), str(data[0]), str(data[1]))
		print add_record
		payload = {"sql": add_record, "key": auth.get_access_token()}
		headers = {"Content-Type": "application/x-www-form-urlencoded"}
		r = requests.post("https://www.googleapis.com/fusiontables/v2/query", payload, headers=headers)
		response = r.json()
		if 'error' in response:
			print "[FusionTable] Nastala chyba pri odosielani poziadavky: " + response['error']['message']
			return False
		else:
			print("[FusionTable] Zaznam bol uspesne odoslany!")
			return True