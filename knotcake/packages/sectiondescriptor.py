from struct import Struct

class SectionDescriptor(Struct):
	def __init__(self):
		self.offset  = 0
		self.length  = 0
		self.type    = ""
		
		self.section = None
	
	def serialize(self, streamWriter):
		super(SectionDescriptor, self).serialize(streamWriter)
		
		if self.section is not None:
			self.offset = self.section.streamStartPosition
			self.length = self.section.streamSize
		
		streamWriter.uint64(self.offset)
		streamWriter.uint64(self.length)
		streamWriter.stringN8(self.type)
	
	def deserialize(self, streamReader):
		super(SectionDescriptor, self).serialize(streamReader)
		
		self.offset = streamReader.uint64()
		self.length = streamReader.uint64()
		self.type   = streamReader.stringN8()
