import struct

# Integers
def uint8ToUInt8s(n):
	return n

def uint16ToUInt8s(n):
	return  n       & 0xFF, \
	       (n >> 8) & 0xFF

def uint32ToUInt8s(n):
	return  n        & 0xFF, \
	       (n >>  8) & 0xFF, \
	       (n >> 16) & 0xFF, \
	       (n >> 24) & 0xFF

def uint64ToUInt8s(n):
	return  n        & 0xFF, \
	       (n >>  8) & 0xFF, \
	       (n >> 16) & 0xFF, \
	       (n >> 24) & 0xFF, \
	       (n >> 32) & 0xFF, \
	       (n >> 40) & 0xFF, \
	       (n >> 48) & 0xFF, \
	       (n >> 56) & 0xFF

def uint8sToUInt8(uint80):
	return uint80

def uint8sToUInt16(uint80, uint81):
	return uint80 + \
	       uint81 << 8

def uint8sToUInt32(uint80, uint81, uint82, uint83):
	return uint80 + \
	       uint81 <<  8 + \
	       uint82 << 16 + \
	       uint83 << 24

def uint8sToUInt64(uint80, uint81, uint82, uint83, uint84, uint85, uint86, uint87):
	return uint80 + \
	       uint81 <<  8 + \
	       uint82 << 16 + \
	       uint83 << 24 + \
	       uint84 << 32 + \
	       uint85 << 40 + \
	       uint86 << 48 + \
	       uint87 << 56

def int8ToUInt8s(n):  return n & 0xFF
def int16ToUInt8s(n): return uint16ToUInt8s(n)
def int32ToUInt8s(n): return uint32ToUInt8s(n)
def int64ToUInt8s(n): return uint64ToUInt8s(n)

def uint8sToInt8(uint80):
	n = uint8sToUInt8(uint80)
	if n >= 128: n = n - 256
	return n

def uint8sToInt16(uint80, uint81):
	n = uint8sToUInt16(uint80, uint81)
	if n > 32768: n = n - 65536
	return n

def uint8sToInt32(uint80, uint81, uint82, uint83):
	n = uint8sToUInt32(uint80, uint81, uint82, uint83)
	if n > 2147483648: n = n - 4294967296
	return n

def uint8sToInt64(uint80, uint81, uint82, uint83, uint84, uint85, uint86, uint87):
	low  = uint8sToUInt32 (uint80, uint81, uint82, uint83)
	high = uint8sToInt32 (uint84, uint85, uint86, uint87)
	return low + high * 4294967296

def uint8ToBytes(n):  return struct.pack("=B", n)
def uint16ToBytes(n): return struct.pack("=H", n)
def uint32ToBytes(n): return struct.pack("=I", n)
def uint64ToBytes(n): return struct.pack("=Q", n)
def int8ToBytes(n):   return struct.pack("=b", n)
def int16ToBytes(n):  return struct.pack("=h", n)
def int32ToBytes(n):  return struct.pack("=i", n)
def int64ToBytes(n):  return struct.pack("=q", n)
def bytesToUInt8(s, offset = 0):  return struct.unpack_from("=B", s, offset)[0]
def bytesToUInt16(s, offset = 0): return struct.unpack_from("=H", s, offset)[0]
def bytesToUInt32(s, offset = 0): return struct.unpack_from("=I", s, offset)[0]
def bytesToUInt64(s, offset = 0): return struct.unpack_from("=Q", s, offset)[0]
def bytesToInt8(s, offset = 0):   return struct.unpack_from("=b", s, offset)[0]
def bytesToInt16(s, offset = 0):  return struct.unpack_from("=h", s, offset)[0]
def bytesToInt32(s, offset = 0):  return struct.unpack_from("=i", s, offset)[0]
def bytesToInt64(s, offset = 0):  return struct.unpack_from("=q", s, offset)[0]

def uint8ToBytesLE(n):  return struct.pack("<B", n)
def uint16ToBytesLE(n): return struct.pack("<H", n)
def uint32ToBytesLE(n): return struct.pack("<I", n)
def uint64ToBytesLE(n): return struct.pack("<Q", n)
def int8ToBytesLE(n):   return struct.pack("<b", n)
def int16ToBytesLE(n):  return struct.pack("<h", n)
def int32ToBytesLE(n):  return struct.pack("<i", n)
def int64ToBytesLE(n):  return struct.pack("<q", n)
def bytesToUInt8LE(s, offset = 0):  return struct.unpack_from("<B", s, offset)[0]
def bytesToUInt16LE(s, offset = 0): return struct.unpack_from("<H", s, offset)[0]
def bytesToUInt32LE(s, offset = 0): return struct.unpack_from("<I", s, offset)[0]
def bytesToUInt64LE(s, offset = 0): return struct.unpack_from("<Q", s, offset)[0]
def bytesToInt8LE(s, offset = 0):   return struct.unpack_from("<b", s, offset)[0]
def bytesToInt16LE(s, offset = 0):  return struct.unpack_from("<h", s, offset)[0]
def bytesToInt32LE(s, offset = 0):  return struct.unpack_from("<i", s, offset)[0]
def bytesToInt64LE(s, offset = 0):  return struct.unpack_from("<q", s, offset)[0]

def uint8ToBytesBE(n):  return struct.pack(">B", n)
def uint16ToBytesBE(n): return struct.pack(">H", n)
def uint32ToBytesBE(n): return struct.pack(">I", n)
def uint64ToBytesBE(n): return struct.pack(">Q", n)
def int8ToBytesBE(n):   return struct.pack(">b", n)
def int16ToBytesBE(n):  return struct.pack(">h", n)
def int32ToBytesBE(n):  return struct.pack(">i", n)
def int64ToBytesBE(n):  return struct.pack(">q", n)
def bytesToUInt8BE(s, offset = 0):  return struct.unpack_from(">B", s, offset)[0]
def bytesToUInt16BE(s, offset = 0): return struct.unpack_from(">H", s, offset)[0]
def bytesToUInt32BE(s, offset = 0): return struct.unpack_from(">I", s, offset)[0]
def bytesToUInt64BE(s, offset = 0): return struct.unpack_from(">Q", s, offset)[0]
def bytesToInt8BE(s, offset = 0):   return struct.unpack_from(">b", s, offset)[0]
def bytesToInt16BE(s, offset = 0):  return struct.unpack_from(">h", s, offset)[0]
def bytesToInt32BE(s, offset = 0):  return struct.unpack_from(">i", s, offset)[0]
def bytesToInt64BE(s, offset = 0):  return struct.unpack_from(">q", s, offset)[0]

# IEEE floating point numbers
def floatToBytes(f):  return struct.pack("=f", f)
def doubleToBytes(f): return struct.pack("=d", f)
def bytesToFloat(s, offset = 0):  return struct.unpack_from("=f", s, offset)[0]
def bytesToDouble(s, offset = 0): return struct.unpack_from("=d", s, offset)[0]

def floatToBytesLE(f):  return struct.pack("<f", f)
def doubleToBytesLE(f): return struct.pack("<d", f)
def bytesToFloatLE(s, offset = 0):  return struct.unpack_from("<f", s, offset)[0]
def bytesToDoubleLE(s, offset = 0): return struct.unpack_from("<d", s, offset)[0]

def floatToBytesBE(f):  return struct.pack(">f", f)
def doubleToBytesBE(f): return struct.pack(">d", f)
def bytesToFloatBE(s, offset = 0):  return struct.unpack_from(">f", s, offset)[0]
def bytesToDoubleBE(s, offset = 0): return struct.unpack_from(">d", s, offset)[0]

# Strings
def stringToBytes(s):
	if isinstance(s, bytes): return s
	if isinstance(s, bytearray): return s
	if isinstance(s, str): return s
	if isinstance(s, unicode): return s.encode("utf-8")
	raise TypeError()

def bytesToString(s):
	return bytes(s)
