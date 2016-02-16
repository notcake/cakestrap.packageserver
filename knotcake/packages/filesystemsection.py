from section import Section

class FileSystemSection(Section):
	def __init__(self):
		from filesystemdirectory import FileSystemDirectory
		
		super(FileSystemSection, self).__init__()
		
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
		return "filesystem"
	
	# FileSystemSection
	@classmethod
	def fromDirectoryTree(cls, directoryTree):
		fileSystemSection = cls()
		fileSystemSection.directoryTree = directoryTree
		return fileSystemSection
