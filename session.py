import random
import string

class Session(object):
	def __init__(self, session):
		self.session = session
	
	# Login
	def logIn(self, userId):
		self.session["userId"] = userId
		self.session["csrfToken"] = None # Force CSRF token regneration
	
	def logOut(self):
		self.session["userId"] = None
		self.session["csrfToken"] = None # Force CSRF token regneration
	
	def isLoggedIn(self):
		if "userId" not in self.session: return False
		return self.session["userId"] is not None
	
	@property
	def userId(self):
		return self.session["userId"]
	
	# CSRF token
	@property
	def csrfToken(self):
		if "csrfToken" not in self.session: self.generateCrsfToken()
		if self.session["csrfToken"] is None: self.generateCsrfToken()
		return self.session["csrfToken"]
	
	def generateCsrfToken(self):
		self.session["csrfToken"] = "".join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(32))
	
	def invalidateCsrfToken(self):
		self.session["csrfToken"] = None