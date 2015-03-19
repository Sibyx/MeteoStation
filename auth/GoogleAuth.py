__author__ = 'Jakub Dubec'
import requests
import time
from config import config


class GoogleAuth:
	def get_device_code(self):
		payload = {"client_id": config.get("Google", "client_id"), "scope": config.get("Google", "scopes")}
		headers = {"Content-Type": "application/x-www-form-urlencoded"}
		r = requests.post(config.get("Google", "auth_endpoint"), payload, headers=headers)
		response = r.json()
		if 'error' in response:
			print "[Auth] Error response from Google server: " + response['error_description']
			return False
		else:
			print("[Auth] Authorization code: " + response['user_code'])
			print("[Auth] Verification URL: " + response['verification_url'])
			return response

	def refresh_token(self):
		payload = {
			"client_id": config.get("Google", "client_id"),
			"client_secret": config.get("Google", "client_secret"),
			"refresh_token": config.get("Token", "refresh_token"),
			"grant_type": "refresh_token"
		}
		headers = {"Content-Type": "application/x-www-form-urlencoded"}
		r = requests.post(config.get("Google", "token_endpoint"), payload, headers=headers)
		response = r.json()
		if 'error' in response:
			print "[Auth] Error response from Google server: " + response['error_description']
			return False
		else:
			print("[Auth] New access token received")
			config.set("Token", "access_token", response['access_token'])
			config.set("Token", "expires", str(int(time.time()) + response['expires_in']))
			return True

	def authorize(self):
		"""

		:rtype : bool
		"""
		code = self.get_device_code()
		if not code:
			return False
		elapsed = 0
		while elapsed < code['expires_in']:
			payload = {
				"client_id": config.get("Google", "client_id"),
				"client_secret": config.get("Google", "client_secret"),
				"code": code['device_code'],
				"grant_type": "http://oauth.net/grant_type/device/1.0"
			}
			headers = {"Content-Type": "application/x-www-form-urlencoded"}
			r = requests.post(config.get("Google", "token_endpoint"), payload, headers=headers)
			response = r.json()
			if 'error' in response:
				if response['error'] == 'authorization_pending':
					time.sleep(code['interval'])
				elif response['error'] == 'slow_down':
					code['interval'] += 1
					time.sleep(code['interval'])
			else:
				print("[Auth] New access token received")
				config.set("Token", "access_token", response['access_token'])
				config.set("Token", "refresh_token", response['refresh_token'])
				config.set("Token", "expires", str(int(time.time()) + response['expires_in']))
				return True
			elapsed += code['interval']
		return False

	def get_access_token(self):
		if config.get("Token", "refresh_token") == "0":
			self.authorize()
		if int(time.time()) > config.getint("Token", "expires"):
			self.refresh_token()
		return config.get("Token", "access_token")

auth = GoogleAuth()