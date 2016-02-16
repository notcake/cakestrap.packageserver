import os

from streamreader import StreamReader

class FileInStream(StreamReader):
	def __init__(self, file):
		super(FileInStreamn, self).__init__()
		
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
	
	# IInStream
	def read(self, size):
		return self.file.read(size)
	
	# FileInStream
	def flush(self):
		self.file.flush()
