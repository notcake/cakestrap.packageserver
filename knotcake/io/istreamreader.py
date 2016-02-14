from knotcake.oop import abstract

from iinstream import IInStream

class IStreamReader(IInStream):
	# IInStream
	def toStreamReader(self):
		return self
	
	# IStreamReader
	@property
	@abstract
	def endianness(self): pass
	
	@endianness.setter
	@abstract
	def endianness(self, endianness): pass
	
	@abstract
	def uint8(self): pass
	@abstract
	def uint16(self): pass
	@abstract
	def uint32(self): pass
	@abstract
	def uint64(self): pass
	
	@abstract
	def int8(self): pass
	@abstract
	def int16(self): pass
	@abstract
	def int32(self): pass
	@abstract
	def int64(self): pass
	
	@abstract
	def uint8LE(self): pass
	@abstract
	def uint16LE(self): pass
	@abstract
	def uint32LE(self): pass
	@abstract
	def uint64LE(self): pass
	
	@abstract
	def int8LE(self): pass
	@abstract
	def int16LE(self): pass
	@abstract
	def int32LE(self): pass
	@abstract
	def int64LE(self): pass
	
	@abstract
	def uint8BE(self): pass
	@abstract
	def uint16BE(self): pass
	@abstract
	def uint32BE(self): pass
	@abstract
	def uint64BE(self): pass
	
	@abstract
	def int8BE(self):  pass
	@abstract
	def int16BE(self): pass
	@abstract
	def int32BE(self): pass
	@abstract
	def int64BE(self): pass
	
	@abstract
	def float(self):  pass
	@abstract
	def double(self): pass
	
	@abstract
	def floatLE(self): pass
	@abstract
	def doubleLE(self): pass
	
	@abstract
	def floatBE(self): pass
	@abstract
	def doubleBE(self): pass
	
	@abstract
	def boolean(self): pass
	
	@abstract
	def bytes(self, length): pass
	
	@abstract
	def stringN8(self): pass
	@abstract
	def stringN16(self): pass
	@abstract
	def stringN32(self): pass
	
	@abstract
	def stringN8LE(self): pass
	@abstract
	def stringN16LE(self): pass
	@abstract
	def stringN32LE(self): pass
	
	@abstract
	def stringN8BE(self): pass
	@abstract
	def stringN16BE(self): pass
	@abstract
	def stringN32BE(self): pass
	
	@abstract
	def stringZ(self): pass
