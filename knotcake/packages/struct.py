import functools

import knotcake.oop

class MetaStruct(type):
	@staticmethod
	def wrapSerializer(f):
		@functools.wraps(f)
		def serializer(self, streamReaderWriter):
			self.streamStartPosition = streamReaderWriter.position
			f(self, streamReaderWriter)
			self.streamEndPosition = streamReaderWriter.position
		
		return serializer
	
	def __new__(cls, name, bases, attrs):
		if "serialize" in attrs:
			attrs["serialize"] = cls.wrapSerializer(attrs["serialize"])
		
		if "deserialize" in attrs:
			attrs["deserialize"] = cls.wrapSerializer(attrs["deserialize"])
		
		return super(MetaStruct, cls).__new__(cls, name, bases, attrs)

class Struct(knotcake.oop.Object):
	__metaclass__ = MetaStruct
	
	def __init__(self):
		self.streamStartPosition = 0
		self.streamEndPosition = 0
	
	@property
	def streamSize(self):
		return self.streamEndPosition - self.streamStartPosition
	
	def serialize(self, streamWriter): pass
	def deserialize(self, streamReader): pass
