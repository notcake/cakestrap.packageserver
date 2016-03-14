from knotcake.oop import abstract

from ibasestream import IBaseStream

class IOutStream(IBaseStream):
	@abstract
	def write(self, data, length = None): pass
	
	def toStreamWriter(self):
		from bufferedstreamwriter import BufferedStreamWriter
		return BufferedStreamWriter(self)
