from sqlalchemy import select, func
from sqlalchemy import Column, PrimaryKeyConstraint, ForeignKey, UniqueConstraint
from sqlalchemy import Boolean, Integer, BigInteger, Text
from sqlalchemy import Enum
from sqlalchemy.orm import relationship, column_property, reconstructor

from knotcake.oop import abstract, instance

from idirectorytree import IDirectoryTree

class IRepositoryTree(IDirectoryTree):
	__abstract__ = True
	
	@property
	@abstract
	def repositoryUrl(self): pass
	
	@abstract
	def getRepositoryUrl(self): pass
	
	@abstract
	def setRepositoryUrl(self, databaseSession, repositoryUrl): pass
	
	# Static
	@classmethod
	@abstract
	def create(cls, databaseSession, repositoryUrl): pass
