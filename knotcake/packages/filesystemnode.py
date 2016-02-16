from knotcake.oop import abstract

from struct import Struct

from filesystemnodetype import FileSystemNodeType

class FileSystemNode(Struct):
	def __init__(self):
		super(FileSystemNode, self).__init__()
		
		self.type = FileSystemNodeType.Invalid
		self.name = ""
	
	# Struct
	def serialize(self, streamWriter):
		super(FileSystemNode, self).serialize(streamWriter)
		
		streamWriter.uint8(self.type)
		streamWriter.stringN8(self.name)
	
	def deserialize(self, streamReader):
		super(FileSystemNode, self).serialize(streamReader)
		
		self.type = streamReader.uint8()
		self.name = streamReader.stringN8()
	
	@classmethod
	def deserializeInstance(cls, self, streamReader):
		from filesystemdirectory import FileSystemDirectory
		from filesystemfile      import FileSystemFile
		
		position = streamReader.position
		type = streamReader.uint8()
		streamReader.seekTo(position)
		
		fileSystemNode = None
		if type == FileSystemNodeType.Directory:
			fileSystemNode = FileSystemDirectory()
		elif type == FileSystemNodeType.File:
			fileSystemNode = FileSystemFile()
		else:
			fileSystemNode = cls()
		
		fileSystemNode.deserialize(streamReader)
		return fileSystemNode
