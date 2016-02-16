from filesystemnodetype import FileSystemNodeType
from filesystemnode     import FileSystemNode

class FileSystemFile(FileSystemNode):
	def __init__(self):
		super(FileSystemFile, self).__init__()
		
		self.type     = FileSystemNodeType.File
		self.offset   = 0
		self.size     = 0
		self.content  = None
		
		self.path     = None
	
	# Struct
	def serialize(self, streamWriter):
		super(FileSystemFile, self).serialize(streamWriter)
		
		offsetPosition = streamWriter.position
		streamWriter.uint64(0)
		
		content = None
		if self.path is not None:
			f = open(self.path, "rb")
			content = f.read()
			f.close()
			
			self.size = len(content)
		else:
			content = self.content
		
		streamWriter.uint64(self.size)
		offset = streamWriter.position
		streamWriter.bytes(content)
		
		streamEndPosition = streamWriter.position
		streamWriter.seekAbsolute(offsetPosition)
		streamWriter.uint64(offset)
		streamWriter.seekAbsolute(streamEndPosition)
	
	def deserialize(self, streamReader):
		super(FileSystemDirectory, self).serialize(streamReader)
		
		self.offset = streamReader.uint64()
		self.size   = streamReader.uint64()
	
	# FileSystemFile
	def assimilate(self, path):
		self.path = path
