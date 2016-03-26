import os

import knotcake.bitconverter

from streamwriter import StreamWriter

class StringOutputStream(StreamWriter):
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
	
	# IOutputStream
	def write(self, data, length = None):
		data = knotcake.bitconverter.stringToBytes(data)
		if length is None: length = len(data)
		if length < len(data): data = data[0:length]
		
		self.data[self.position:(self.position + len(data))] = data
	
	# StringOutputStream
	def clear(self):
		self.data = bytearray()
		self._position = 0
	
	def toString(self):
		return self.data
