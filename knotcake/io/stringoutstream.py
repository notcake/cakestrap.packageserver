import os

import knotcake.bitconverter

from streamwriter import StreamWriter

class StringOutStream(StreamWriter):
	def __init__(self):
		self.data = bytearray()
		self._position = 0
	
	# IBaseStream
	def close(self):
		self.data = bytearray()
	
	@property
	def position(self):
		return self._position
	
	@property
	def size(self):
		return len(self.data)
	
	def seekAbsolute(self, seekPos):
		seekPos = max(seekPos, self.size)
		self._position = seekPos
	
	# IOutStream
	def write(self, data, size = None):
		data = knotcake.bitconverter.stringToBytes(data)
		if size is None: size = len(data)
		if size < len(data): data = data[0:size]
		
		self.data[self.position:(self.position + len(data))] = data
	
	# StringOutStream
	def clear(self):
		self.data = bytearray()
		self._position = 0
	
	def toString(self):
		return self.data
