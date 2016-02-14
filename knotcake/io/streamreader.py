import struct

from knotcake.oop import abstract
import knotcake.bitconverter

from endianness import Endianness
from istreamreader import IStreamReader

class StreamReader(IStreamReader):
	def __init__(self):
		super(StreamReader, self).__init__()
		
		self._endianness = None
		self.endianness = Endianness.LittleEndian
	
	# IStreamReader
	@property
	def endianness(self):
		return self._endianness
	
	@endianness.setter
	def endianness(self, endianness):
		if self._endianness == endianness: return self
		
		self._endianness = endianness
		
		if self._endianness == Endianness.LittleEndian:
			self.uint16    = self.uint16LE
			self.uint32    = self.uint32LE
			self.uint64    = self.uint64LE
			self.int16     = self.int16LE
			self.int32     = self.int32LE
			self.int64     = self.int64LE
			self.float     = self.floatLE
			self.double    = self.doubleLE
			self.stringN8  = self.stringN8LE
			self.stringN16 = self.stringN16LE
			self.stringN32 = self.stringN32LE
		else:
			self.uint16    = self.uint16BE
			self.uint32    = self.uint32BE
			self.uint64    = self.uint64BE
			self.int16     = self.int16BE
			self.int32     = self.int32BE
			self.int64     = self.int64BE
			self.float     = self.floatBE
			self.double    = self.doubleBE
			self.stringN8  = self.stringN8BE
			self.stringN16 = self.stringN16BE
			self.stringN32 = self.stringN32BE
		
		return self
	
	def uint8(self):    uint80 = self.uint81(); return knotcake.bitconverter.uint8sToUInt8(uint80 or 0)
	def uint8LE(self):  uint80 = self.uint81(); return knotcake.bitconverter.uint8sToUInt8(uint80 or 0)
	def uint8BE(self):  uint80 = self.uint81(); return knotcake.bitconverter.uint8sToUInt8(uint80 or 0)
	def int8(self):     uint80 = self.uint81(); return knotcake.bitconverter.uint8sToInt8(uint80 or 0)
	def int8LE(self):   uint80 = self.uint81(); return knotcake.bitconverter.uint8sToInt8(uint80 or 0)
	def int8BE(self):   uint80 = self.uint81(); return knotcake.bitconverter.uint8sToInt8(uint80 or 0)
	
	def uint16LE(self): uint80, uint81 = self.uint82(); return knotcake.bitconverter.uint8sToUInt16(uint80 or 0, uint81 or 0)
	def uint16BE(self): uint80, uint81 = self.uint82(); return knotcake.bitconverter.uint8sToUInt16(uint81 or 0, uint80 or 0)
	def int16LE(self):  uint80, uint81 = self.uint82(); return knotcake.bitconverter.uint8sToInt16(uint80 or 0, uint81 or 0)
	def int16BE(self):  uint80, uint81 = self.uint82(); return knotcake.bitconverter.uint8sToInt16(uint81 or 0, uint80 or 0)
	
	def uint32LE(self): uint80, uint81, uint82, uint83 = self.uint84(); return knotcake.bitconverter.uint8sToUInt32(uint80 or 0, uint81 or 0, uint82 or 0, uint83 or 0)
	def uint32BE(self): uint80, uint81, uint82, uint83 = self.uint84(); return knotcake.bitconverter.uint8sToUInt32(uint83 or 0, uint82 or 0, uint81 or 0, uint80 or 0)
	def int32LE(self):  uint80, uint81, uint82, uint83 = self.uint84(); return knotcake.bitconverter.uint8sToInt32(uint80 or 0, uint81 or 0, uint82 or 0, uint83 or 0)
	def int32BE(self):  uint80, uint81, uint82, uint83 = self.uint84(); return knotcake.bitconverter.uint8sToInt32(uint83 or 0, uint82 or 0, uint81 or 0, uint80 or 0)
	
	def uint64LE(self): uint80, uint81, uint82, uint83, uint84, uint85, uint86, uint87 = self.uint88(); return knotcake.bitconverter.uint8sToUInt32(uint80 or 0, uint81 or 0, uint82 or 0, uint83 or 0, uint84 or 0, uint85 or 0, uint86 or 0, uint87 or 0)
	def uint64BE(self): uint80, uint81, uint82, uint83, uint84, uint85, uint86, uint87 = self.uint88(); return knotcake.bitconverter.uint8sToUInt32(uint87 or 0, uint86 or 0, uint85 or 0, uint84 or 0, uint83 or 0, uint82 or 0, uint81 or 0, uint80 or 0)
	def int64LE(self):  uint80, uint81, uint82, uint83, uint84, uint85, uint86, uint87 = self.uint88(); return knotcake.bitconverter.uint8sToInt32(uint80 or 0, uint81 or 0, uint82 or 0, uint83 or 0, uint84 or 0, uint85 or 0, uint86 or 0, uint87 or 0)
	def int64BE(self):  uint80, uint81, uint82, uint83, uint84, uint85, uint86, uint87 = self.uint88(); return knotcake.bitconverter.uint8sToInt32(uint87 or 0, uint86 or 0, uint85 or 0, uint84 or 0, uint83 or 0, uint82 or 0, uint81 or 0, uint80 or 0)
	
	def floatLE(self):  return knotcake.bitconverter.bytesToFloatLE(self.read(4))
	def floatBE(self):  return knotcake.bitconverter.bytesToFloatBE(self.read(4))
	def doubleLE(self): return knotcake.bitconverter.bytesToDoubleLE(self.read(8))
	def doubleBE(self): return knotcake.bitconverter.bytesToDoubleBE(self.read(8))
	
	def boolean(self):
		return self.uint8() != 0
	
	def bytes(self, length):
		return self.read(length)
	
	def stringN8LE(self):  return self.bytes(self.uint8LE())
	def stringN16LE(self): return self.bytes(self.uint16LE())
	def stringN32LE(self): return self.bytes(self.uint32LE())
	def stringN8BE(self):  return self.bytes(self.uint8BE())
	def stringN16BE(self): return self.bytes(self.uint16BE())
	def stringN32BE(self): return self.bytes(self.uint32BE())
	
	def stringZ(self):
		data = bytearray()
		c = self.uint8()
		while c and c != 0:
			if len(data) > 65536:
				raise Error("StreamReader:StringZ : String is too long, infinite loop?")
				break
			
			data.append(c)
			c = self.uint8()
		
		return data
	
	# StreamReader
	# Internal
	def uint81(self):
		return struct.unpack("B", self.read(1))[0]
	
	def uint82(self):
		return struct.unpack("BB", self.read(2))
	
	def uint84(self):
		return struct.unpack("BBBB", self.read(4))
	
	def uint88(self):
		return struct.unpack("BBBBBBBB", self.read(8))
