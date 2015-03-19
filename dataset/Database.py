__author__ = 'Jakub Dubec'
import mysql.connector
from config import config


class Database:

	conn = None

	def __init__(self):
		self.conn = mysql.connector.connect(
			host=config.get("Database", "host"),
			user=config.get("Database", "user"),
			password=config.get("Database", "password"),
			database=config.get("Database", "schema")
		)
		if self.conn.is_connected():
			print("[Databaza] Pripojil som sa k {0}".format(self.conn.server_host))

	def insert(self, temperature, humidity):
		cursor = self.conn.cursor()
		add_record = "INSERT INTO measurement (mst_date, mst_temperature, mst_humidity) VALUES (NOW(), %s, %s)"
		cursor.execute(add_record, temperature, humidity)
		print("[Databaza] Odoslane merianie cislo {0}".format(cursor.lastrowid))
		self.conn.commit()
		cursor.close()

	def __exit__(self, exc_type, exc_val, exc_tb):
		self.conn.close()