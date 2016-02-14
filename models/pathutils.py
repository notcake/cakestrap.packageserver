import re

class PathUtils:
	@staticmethod
	def createFileName(x):
		return re.sub(r"[^a-zA-Z0-9\.]+", u"_", x)
