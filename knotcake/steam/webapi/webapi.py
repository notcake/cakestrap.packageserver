import json
import requests

from user import User

class WebApi(object):
	def __init__(self, apiKey):
		self.apiKey = apiKey
		
		self.usersBySteamId64 = {}
	
	def getUserBySteamId64(self, steamId64):
		if steamId64 not in self.usersBySteamId64:
			url = "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=" + self.apiKey + "&steamids=" + str(steamId64)
			for userInformation in self.get(url)["players"]:
				if int(userInformation["steamid"]) not in self.usersBySteamId64:
					user = User.fromUserInformation(userInformation)
					self.usersBySteamId64[user.steamId64] = user
				
		return self.usersBySteamId64.get(steamId64)
	
	def get(self, url):
		response = requests.get(url)
		response = json.loads(response.content)
		return response["response"]
