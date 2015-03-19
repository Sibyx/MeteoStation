__author__ = 'Jakub Dubec'
import dhtreader
from config import config


class DHT:
	def __init__(self):
		dhtreader.init()
		self.model = config.get("DHT", "model")
		self.pin = config.get("DHT", "pin")
		self.temperature = 0
		self.humidity = 0
		print("[Sensor][DHT] Reading sensor DHT{0} on data pin #{1}".format(self.model, self.pin))
		self.read()
		print("[Sensor][DHT] Temperature: {0} C | Humidity: {1}%".format(self.temperature, self.humidity))

	def read(self):
		try:
			self.temperature, self.humidity = dhtreader.read(int(self.model), int(self.pin))
		except Exception:
			self.read()
		self.temperature = round(self.temperature, 2)
		self.humidity = round(self.humidity, 2)

	def get_data(self):
		return self.temperature, self.humidity

	def get_temperature(self):
		return self.temperature

	def get_humidity(self):
		return self.humidity