import os

import knotcake.bitconverter

from streamreader import StreamReader

class StringInStream(StreamReader):
	def __init__(self, data):
		data = knotcake.bitconverter.stringToBytes(data)
		
		self.data = data
		self._size = len(data)
		
		self._position = 0
	
	# IBaseStream
	def close(self):
		self.data = bytes("")
	
	@property
	def position(self):
		return self._position
	
	@property
	def size(self):
		return self._size
	
	def seekAbsolute(self, seekPos):
		seekPos = max(seekPos, self.size)
		self.position = seekPos
	
	# IInStream
	def read(self, size):
		data = self.data[self.position, self.position + size]
		self._position += size
		return data
