import certifi
import re
import urllib
import urllib3

import knotcake.oop

httpPoolManager = urllib3.PoolManager(cert_reqs = "CERT_REQUIRED", ca_certs = certifi.where())

class OpenId(knotcake.oop.Object):
	def __init__(self):
		self.localIdentity = None
		self.returnUrl     = None
	
	def generateLoginUrl(self):
		parameters = {
			"openid.ns":         "http://specs.openid.net/auth/2.0",
			"openid.mode":       "checkid_setup",
			"openid.return_to":  self.returnUrl,
			"openid.realm":      self.localIdentity,
			"openid.identity":   "http://specs.openid.net/auth/2.0/identifier_select",
			"openid.claimed_id": "http://specs.openid.net/auth/2.0/identifier_select"
		}
		parameters = { k: urllib.quote(v, "") for k, v in parameters.iteritems() }
		parameters = [ k + "=" + v for k, v in parameters.iteritems() ]
		parameters = str.join("&", parameters)
		return "https://steamcommunity.com/openid/login?" + parameters
	
	def validateLogin(self, parameters):
		signedParameters = ["openid." + parameterName for parameterName in parameters["openid.signed"].split(",")]
		validationParameters = { parameterName: parameters[parameterName] for parameterName in signedParameters }
		validationParameters["openid.ns"]           = "http://specs.openid.net/auth/2.0"
		validationParameters["openid.signed"]       = parameters["openid.signed"]
		validationParameters["openid.sig"]          = parameters["openid.sig"]
		validationParameters["openid.assoc_handle"] = parameters["openid.assoc_handle"]
		validationParameters["openid.mode"]         = "check_authentication"
		
		validationParameters = { k: urllib.quote(v, "") for k, v in validationParameters.iteritems() }
		validationParameters = [ k + "=" + v for k, v in validationParameters.iteritems() ]
		validationParameters = str.join("&", validationParameters )
		
		response = httpPoolManager.request(
			"POST",
			"https://steamcommunity.com/openid/login",
			body = validationParameters,
			headers = {
				"Accept-Language": "en",
				"Content-Type": "application/x-www-form-urlencoded"
			}
		)
		
		if "is_valid:true" not in response.data: return None
		if "openid.return_to" not in parameters: return None
		if parameters["openid.return_to"] != self.returnUrl: return None
		
		match = re.match(r"^http://steamcommunity.com/openid/id/([0-9]+)$", parameters["openid.claimed_id"])
		
		return int(match.group(1))
