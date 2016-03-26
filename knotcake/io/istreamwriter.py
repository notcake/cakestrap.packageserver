from knotcake.oop import abstract

from ioutputstream import IOutputStream

class IStreamWriter(IOutputStream):
	# IOutputStream
	def toStreamWriter(self):
		return self
	
	# IStreamWriter
	@property
	@abstract
	def endianness(self): pass
	
	@endianness.setter
	@abstract
	def endianness(self, endianness): pass
	
	@abstract
	def uint8(self, n): pass
	@abstract
	def uint16(self, n): pass
	@abstract
	def uint32(self, n): pass
	@abstract
	def uint64(self, n): pass
	
	@abstract
	def int8(self, n): pass
	@abstract
	def int16(self, n): pass
	@abstract
	def int32(self, n): pass
	@abstract
	def int64(self, n): pass
	
	@abstract
	def uint8LE(self, n): pass
	@abstract
	def uint16LE(self, n): pass
	@abstract
	def uint32LE(self, n): pass
	@abstract
	def uint64LE(self, n): pass
	
	@abstract
	def int8LE(self, n): pass
	@abstract
	def int16LE(self, n): pass
	@abstract
	def int32LE(self, n): pass
	@abstract
	def int64LE(self, n): pass
	
	@abstract
	def uint8BE(self, n): pass
	@abstract
	def uint16BE(self, n): pass
	@abstract
	def uint32BE(self, n): pass
	@abstract
	def uint64BE(self, n): pass
	
	@abstract
	def int8BE(self, n):  pass
	@abstract
	def int16BE(self, n): pass
	@abstract
	def int32BE(self, n): pass
	@abstract
	def int64BE(self, n): pass
	
	@abstract
	def float(self, f):  pass
	@abstract
	def double(self, f): pass
	
	@abstract
	def floatLE(self, f): pass
	@abstract
	def doubleLE(self, f): pass
	
	@abstract
	def floatBE(self, f): pass
	@abstract
	def doubleBE(self, f): pass
	
	@abstract
	def boolean(self, b): pass
	
	@abstract
	def bytes(self, data, length = None): pass
	
	@abstract
	def stringN8(self, s): pass
	@abstract
	def stringN16(self, s): pass
	@abstract
	def stringN32(self, s): pass
	
	@abstract
	def stringN8LE(self, s): pass
	@abstract
	def stringN16LE(self, s): pass
	@abstract
	def stringN32LE(self, s): pass
	
	@abstract
	def stringN8BE(self, s): pass
	@abstract
	def stringN16BE(self, s): pass
	@abstract
	def stringN32BE(self, s): pass
	
	@abstract
	def stringZ(self, s): pass
