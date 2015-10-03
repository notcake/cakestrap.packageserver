import random
import string

class Session(object):
	def __init__(self, session):
		self.session = session
	
	def logIn(self, userId):
		self.session["userId"] = userId
		self.session["csrfToken"] = "".join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(32))
	
	def logOut(self):
		self.session["userId"] = None
		self.session["csrfToken"] = None
	
	def isLoggedIn(self):
		if "userId" not in self.session: return False
		return self.session["userId"] is not None
	
	@property
	def userId(self):
		return self.session["userId"]
