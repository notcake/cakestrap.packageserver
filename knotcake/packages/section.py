from knotcake.oop import abstract

from struct import Struct

class Section(Struct):
	def __init__(self):
		super(Section, self).__init__()
	
	# Struct
	def serialize(self, streamWriter):
		super(Section, self).serialize(streamWriter)
	
	def deserialize(self, streamReader):
		super(Section, self).serialize(streamReader)
	
	# Section
	@property
	@abstract
	def type(self): pass
