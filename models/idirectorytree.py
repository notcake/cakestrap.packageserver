from sqlalchemy import select, func
from sqlalchemy import Column, PrimaryKeyConstraint, ForeignKey, UniqueConstraint
from sqlalchemy import Boolean, Integer, BigInteger, Text
from sqlalchemy import Enum
from sqlalchemy.orm import relationship, column_property, reconstructor

from knotcake.oop import abstract, instance

from base import Base

class IDirectoryTree(Base):
	__abstract__ = True
	
	@abstract
	def clone(self, clone): pass
	
	@abstract
	def copy(self, source): pass
	
	@abstract
	def createPermalink(self): pass
	
	@property
	@abstract
	def garbageCollectable(self): pass
	
	@instance
	@abstract
	def equals(a, b): pass
	
	@abstract
	def remove(self, databaseSession): pass
	
	@abstract
	def fromFormFieldsDictionary(self, databaseSession, dictionary): pass
	
	@abstract
	def toDictionary(self, out = None): pass
	
	@abstract
	def lockDirectory(self): pass
	
	@abstract
	def unlockDirectory(self): pass
	
	# Static
	@classmethod
	@abstract
	def validateFormFieldsDictionary(cls, dictionary): pass
