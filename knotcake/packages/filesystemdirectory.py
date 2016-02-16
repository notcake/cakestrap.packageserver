import os.path

from filesystemnodetype import FileSystemNodeType
from filesystemnode     import FileSystemNode

class FileSystemDirectory(FileSystemNode):
	def __init__(self):
		super(FileSystemDirectory, self).__init__()
		
		self.type     = FileSystemNodeType.Directory
		self.children = []
		self.childrenOffets = []
	
	# Struct
	def serialize(self, streamWriter):
		super(FileSystemDirectory, self).serialize(streamWriter)
		
		streamWriter.uint16(len(self.children))
		childrenOffsetsPosition = streamWriter.position
		for childNode in self.children:
			streamWriter.uint64(0)
		
		for childNode in self.children:
			childNode.serialize(streamWriter)
		
		streamEndPosition = streamWriter.position
		streamWriter.seekAbsolute(childrenOffsetsPosition)
		self.childrenOffsets = []
		for childNode in self.children:
			self.childrenOffsets.append(childNode.streamStartPosition)
			streamWriter.uint64(childNode.streamStartPosition)
		
		streamWriter.seekAbsolute(streamEndPosition)
	
	def deserialize(self, streamReader):
		super(FileSystemDirectory, self).serialize(streamReader)
		
		childCount = streamReader.uint16()
		for i in range(1, childCount):
			offset = streamReader.uint64()
			self.childrenOffsets.append(offset)
	
	# FileSystemDirectory
	def assimilate(self, path):
		from filesystemfile import FileSystemFile
		
		childNames = os.listdir(path)
		for childName in childNames:
			childPath = os.path.join(path, childName)
			childNode = None
			if os.path.isdir(childPath):
				childNode = FileSystemDirectory()
			else:
				childNode = FileSystemFile()
			
			childNode.name = childName
			childNode.assimilate(childPath)
			self.children.append(childNode)
