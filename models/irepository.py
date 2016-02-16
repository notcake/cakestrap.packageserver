import os.path
import re

from sqlalchemy import select, func
from sqlalchemy import Column, PrimaryKeyConstraint, ForeignKey, UniqueConstraint
from sqlalchemy import Boolean, Integer, BigInteger, Text
from sqlalchemy import Enum
from sqlalchemy.orm import relationship, column_property, reconstructor

from knotcake.oop import abstract, instance
import knotcake.concurrency

from base import Base

class IRepository(Base):
	__abstract__ = True
	
	id              = None
	url             = None
	directoryName   = None
	
	repositoryTrees = None
	
	@abstract
	def gc(self, databaseSession): pass
	
	@abstract
	def getFullPath(self): pass
	
	@abstract
	def getHeadRevision(self, repositoryTree): pass
	
	@property
	@abstract
	def redactedUrl(self): pass
	
	# Static
	@classmethod
	@abstract
	def create(cls, databaseSession, url): pass
	
	# References
	@classmethod
	@abstract
	def setRepository(cls, databaseSession, repositoryUrl, repositoryTree): pass
	
	@classmethod
	@abstract
	def getByUrl(cls, databaseSession, url): pass
	
	@classmethod
	@abstract
	def getByDirectoryName(cls, databaseSession, directoryName): pass
