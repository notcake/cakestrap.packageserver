import functools

def abstract(f):
	@functools.wraps(f)
	def abstract(*args, **kwargs):
		f(*args, **kwargs)
		raise NotImplementedError()
	
	return abstract

class instance(object):
	def __init__(self, method):
		self.method = method
	
	def __get__(self, obj = None, type = None):
		if obj is not None:
			@functools.wraps(self.method)
			def static(*args, **kwargs):
				return self.method(obj, *args, **kwargs)
			
			return static
		else:
			@functools.wraps(self.method)
			def static(*args, **kwargs):
				return self.method(*args, **kwargs)
			
			return static
