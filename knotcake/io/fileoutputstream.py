import os

import knotcake.bitconverter

from streamwriter import StreamWriter

class FileOutputStream(StreamWriter):
	def __init__(self, file):
		super(FileOutputStream, self).__init__()
		
		self.file = file
	
	# IBaseStream
	def close(self):
		if self.file is None: return
		
		self.file.close()
		self.file = None
	
	@property
	def position(self):
		return self.file.tell()
	
	@property
	def size(self):
		position = self.file.tell()
		self.file.seek(0, os.SEEK_END)
		size = self.file.tell()
		self.file.seek(position)
		return size
	
	def seekAbsolute(self, seekPos):
		self.file.seek(seekPos)
	
	# IOutputStream
	def write(self, data, size = None):
		data = knotcake.bitconverter.stringToBytes(data)
		if size is None: size = len(data)
		if size < len(data): data = data[0:size]
		
		self.file.write(data)
	
	# FileOutputStream
	def flush(self):
		self.file.flush()
