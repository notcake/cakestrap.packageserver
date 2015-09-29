import urllib

class OpenId(object):
	def __init__(self):
		self.localUrl = None
	
	def generateLoginUrl(self):
		parameters = {
			"openid.ns":         "http://specs.openid.net/auth/2.0",
			"openid.mode":       "checkid_setup",
			"openid.return_to":  "true",
			"openid.realm":      self.localUrl,
			"openid.identity":   "http://specs.openid.net/auth/2.0/identifier_select",
			"openid.claimed_id": "http://specs.openid.net/auth/2.0/identifier_select"
		}
		parameters = { k: urllib.quote(v, "") for k, v in parameters.iteritems() }
		parameters = [ k + "=" + v for k, v in parameters.iteritems() ]
		parameters = str.join("&", parameters)
		return "https://steamcommunity.com/openid/login?" + parameters
	