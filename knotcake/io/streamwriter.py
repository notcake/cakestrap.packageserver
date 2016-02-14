import struct

from knotcake.oop import abstract
import knotcake.bitconverter

from endianness import Endianness
from istreamwriter import IStreamWriter

class StreamWriter(IStreamWriter):
	def __init__(self):
		super(StreamWriter, self).__init__()
		
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
	
	def uint8(self, n):    uint80 = knotcake.bitconverter.uint8ToUInt8s(n); self.uint81(uint80)
	def uint8LE(self, n):  uint80 = knotcake.bitconverter.uint8ToUInt8s(n); self.uint81(uint80)
	def uint8BE(self, n):  uint80 = knotcake.bitconverter.uint8ToUInt8s(n); self.uint81(uint80)
	def int8(self, n):     uint80 = knotcake.bitconverter.int8ToUInt8s(n);  self.uint81(uint80)
	def int8LE(self, n):   uint80 = knotcake.bitconverter.int8ToUInt8s(n);  self.uint81(uint80)
	def int8BE(self, n):   uint80 = knotcake.bitconverter.int8ToUInt8s(n);  self.uint81(uint80)
	
	def uint16LE(self, n): uint80, uint81 = knotcake.bitconverter.uint16ToUInt8s(n); self.uint82(uint80, uint81)
	def uint16BE(self, n): uint80, uint81 = knotcake.bitconverter.uint16ToUInt8s(n); self.uint82(uint81, uint80)
	def int16LE(self, n):  uint80, uint81 = knotcake.bitconverter.int16ToUInt8s(n);  self.uint82(uint80, uint81)
	def int16BE(self, n):  uint80, uint81 = knotcake.bitconverter.int16ToUInt8s(n);  self.uint82(uint81, uint80)
	
	def uint32LE(self, n): uint80, uint81, uint82, uint83 = knotcake.bitconverter.uint32ToUInt8s(n); self.uint84(uint80, uint81, uint82, uint83)
	def uint32BE(self, n): uint80, uint81, uint82, uint83 = knotcake.bitconverter.uint32ToUInt8s(n); self.uint84(uint83, uint82, uint81, uint80)
	def int32LE(self, n):  uint80, uint81, uint82, uint83 = knotcake.bitconverter.int32ToUInt8s(n);  self.uint84(uint80, uint81, uint82, uint83)
	def int32BE(self, n):  uint80, uint81, uint82, uint83 = knotcake.bitconverter.int32ToUInt8s(n);  self.uint84(uint83, uint82, uint81, uint80)
	
	def uint64LE(self, n): uint80, uint81, uint82, uint83, uint84, uint85, uint86, uint87 = knotcake.bitconverter.uint64ToUInt8s(n); self.uint88(uint80, uint81, uint82, uint83, uint84, uint85, uint86, uint87)
	def uint64BE(self, n): uint80, uint81, uint82, uint83, uint84, uint85, uint86, uint87 = knotcake.bitconverter.uint64ToUInt8s(n); self.uint88(uint87, uint86, uint85, uint84, uint83, uint82, uint81, uint80)
	def int64LE(self, n):  uint80, uint81, uint82, uint83, uint84, uint85, uint86, uint87 = knotcake.bitconverter.int64ToUInt8s(n);  self.uint88(uint80, uint81, uint82, uint83, uint84, uint85, uint86, uint87)
	def int64BE(self, n):  uint80, uint81, uint82, uint83, uint84, uint85, uint86, uint87 = knotcake.bitconverter.int64ToUInt8s(n);  self.uint88(uint87, uint86, uint85, uint84, uint83, uint82, uint81, uint80)
	
	def floatLE(self, f):  self.write(knotcake.bitconverter.floatToBytesLE(f))
	def floatBE(self, f):  self.write(knotcake.bitconverter.floatToBytesBE(f))
	def doubleLE(self, f): self.write(knotcake.bitconverter.doubleToBytesLE(f))
	def doubleBE(self, f): self.write(knotcake.bitconverter.doubleToBytesBE(f))
	
	def boolean(self, b):
		self.uint8(1 if b else 0)
	
	def bytes(self, data, length = None):
		return self.write(data, length)
	
	def stringN8LE(self, s):  s = knotcake.bitconverter.stringToBytes(s); self.uint8LE(len(s));  return self.bytes(s)
	def stringN16LE(self, s): s = knotcake.bitconverter.stringToBytes(s); self.uint16LE(len(s)); return self.bytes(s)
	def stringN32LE(self, s): s = knotcake.bitconverter.stringToBytes(s); self.uint32LE(len(s)); return self.bytes(s)
	def stringN8BE(self, s):  s = knotcake.bitconverter.stringToBytes(s); self.uint8BE(len(s));  return self.bytes(s)
	def stringN16BE(self, s): s = knotcake.bitconverter.stringToBytes(s); self.uint16BE(len(s)); return self.bytes(s)
	def stringN32BE(self, s): s = knotcake.bitconverter.stringToBytes(s); self.uint32BE(len(s)); return self.bytes(s)
	
	def stringZ(self, s):
		s = knotcake.bitconverter.stringToBytes(s)
		self.bytes(s)
		self.uint8(0x00)
	
	# StreamWriter
	# Internal
	def uint81(self, uint80):
		self.write(struct.pack("B", uint80))
	
	def uint82(self, uint80, uint81):
		self.write(struct.pack("BB", uint80, uint81))
	
	def uint84(self, uint80, uint81, uint82, uint83):
		self.write(struct.pack("BBBB", uint80, uint81, uint82, uint83))
	
	def uint88(self, uint80, uint81, uint82, uint83, uint84, uint85, uint86, uint87):
		self.write(struct.pack("BBBBBBBB", uint80, uint81, uint82, uint83, uint84, uint85, uint86, uint87))
