from struct import Struct

class PackageRelease(Struct):
	def __init__(self, package = None, packageRelease = None):
		from packagereleaseheader import PackageReleaseHeader
		
		self.fileFormatVersion = 0
		
		self.header             = PackageReleaseHeader(package, packageRelease)
		self.sectionDescriptors = []
	
	# Struct
	def serialize(self, streamWriter):
		super(PackageRelease, self).serialize(streamWriter)
		
		# Version
		streamWriter.uint32(self.fileFormatVersion)
		
		# Header
		self.header.serialize(streamWriter)
		
		# Section descriptors
		streamWriter.uint32(len(self.sectionDescriptors))
		sectionDescriptorsPosition = streamWriter.position
		for sectionDescriptor in self.sectionDescriptors:
			sectionDescriptor.serialize(streamWriter)
		
		for sectionDescriptor in self.sectionDescriptors:
			sectionDescriptor.section.serialize(streamWriter)
		
		endPosition = streamWriter.position
		streamWriter.seekAbsolute(sectionDescriptorsPosition)
		for sectionDescriptor in self.sectionDescriptors:
			sectionDescriptor.serialize(streamWriter)
		
		streamWriter.seekAbsolute(endPosition)
	
	def deserialize(self, streamReader):
		from sectiondescriptor import SectionDescriptor
		
		super(PackageRelease, self).serialize(streamReader)
		
		# Version
		self.fileFormatVersion = streamReader.uint32()
		
		# Header
		self.header.deserialize(streamReader)
		
		# Section descriptors
		sectionCount = streamReader.uint32()
		self.sectionDescriptors = []
		for i in range(0, sectionCount):
			sectionDescriptor = SectionDescriptor()
			sectionDescriptor.deserialize(streamReader)
			self.sectionDescriptors.append(sectionDescriptor)
	
	# PackageRelease
	def addSection(self, section, type = None):
		from sectiondescriptor import SectionDescriptor
		
		if type is None: type = section.type
		
		sectionDescriptor = SectionDescriptor()
		sectionDescriptor.section = section
		sectionDescriptor.type = type
		
		self.sectionDescriptors.append(sectionDescriptor)
