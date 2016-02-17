import os.path

from section import Section

class FileSystemSection(Section):
	def __init__(self):
		from filesystemdirectory import FileSystemDirectory
		
		super(FileSystemSection, self).__init__()
		
		self._type = "filesystem"
		
		self.rootDirectory = FileSystemDirectory()
		
		self.directoryTree = None
	
	# Struct
	def serialize(self, streamWriter):
		super(FileSystemSection, self).serialize(streamWriter)
		
		unlockRequired = False
		if self.directoryTree:
			path = self.directoryTree.lockDirectory()
			if path is not None:
				unlockRequired = True
				
				if os.path.isfile(path):
					extension = os.path.splitext(path)[1]
					file = self.rootDirectory.createFile("_ctor" + extension)
					file.assimilate(path)
				else:
					self.rootDirectory.assimilate(path)
		
		self.rootDirectory.serialize(streamWriter)
		
		if unlockRequired:
			self.directoryTree.unlockDirectory()
	
	def deserialize(self, streamReader):
		super(FileSystemSection, self).serialize(streamReader)
		
		self.rootDirectory.deserialize(streamReader)
	
	# Section
	@property
	def type(self):
		return self._type
	
	# FileSystemSection
	@classmethod
	def fromDirectoryTree(cls, directoryTree, type):
		fileSystemSection = cls()
		fileSystemSection._type = type
		fileSystemSection.directoryTree = directoryTree
		return fileSystemSection
