import knotcake.oop
from knotcake.oop import abstract

class IBaseStream(knotcake.oop.Object):
	@abstract
	def close(self): pass
	
	@property
	@abstract
	def position(self): pass
	
	@property
	@abstract
	def size(self): pass
	
	@abstract
	def seekAbsolute(self, seekPos): pass
		
	def seekRelative(self, relativeSeekPos):
		self.seekAbsolute(self.position + relativeSeekPos)
