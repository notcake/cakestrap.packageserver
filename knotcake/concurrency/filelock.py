import fcntl
import os
import threading

class FileLock(object):
	def __init__(self, path):
		self.path   = path
		self.thread = threading.current_thread()
		
		self.mutex  = threading.Lock()
		self.count  = 0
	
	def lock(self, name = u""):
		assert(self.thread == threading.current_thread())
		
		self.mutex.acquire()
		try:
			if self.count == 0:
				self.file = open(self.path, "wb")
				fcntl.lockf(self.file.fileno(), fcntl.LOCK_EX)
				self.file.seek(0)
				self.file.truncate()
				
				if name != "": name = " " + name
				name = unicode(os.getpid()) + name
				self.file.write(name)
			
			self.count = self.count + 1
		finally:
			self.mutex.release()
	
	def unlock(self):
		assert(self.thread == threading.current_thread())
		
		self.mutex.acquire()
		try:
			assert(self.count > 0)
			
			self.count = self.count - 1
			
			if self.count == 0:
				self.file.seek(0)
				self.file.truncate()
				fcntl.lockf(self.file.fileno(), fcntl.LOCK_UN)
				self.file.close()
				self.file = None
		finally:
			self.mutex.release()
	
	def delete(self):
		os.remove(self.path)
