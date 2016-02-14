from sqlalchemy import select, func
from sqlalchemy import Column, PrimaryKeyConstraint, ForeignKey, UniqueConstraint
from sqlalchemy import Boolean, Integer, BigInteger, Text
from sqlalchemy import Enum
from sqlalchemy.orm import relationship, column_property, reconstructor

from knotcake.oop import instance

from irepositorytree import IRepositoryTree

class RepositoryTree(IRepositoryTree):
	__abstract__ = True
	
	id           = None
	repositoryId = None
	revision     = None
	directory    = None
	
	repository   = None
	
	# IDirectoryTree
	def clone(self, clone):
		if clone is None: clone = type(self)()
		
		clone.copy(self)
		return clone
	
	def copy(self, source):
		self.revision  = source.revision
		self.directory = source.directory
		
		return self
	
	def createPermalink(self):
		permalink = type(self)()
		permalink.repository = self.repository
		permalink.copy(self)
		
		if permalink.revision is None:
			permalink.revision = self.repository.getHeadRevision(self)
		
		return permalink
	
	@property
	def garbageCollectable(self):
		return self.repository
	
	@instance
	def equals(a, b):
		if a == b: return True
		if type(a) != type(b): return False
		
		if a.revision  != b.revision:  return False
		if a.directory != b.directory: return False
		
		return True
	
	def remove(self, databaseSession):
		databaseSession.delete(self)
		self.setRepositoryUrl(databaseSession, None)
	
	def fromFormFieldsDictionary(self, databaseSession, dictionary):
		self.revision  = dictionary.get("revision",  "")
		self.directory = dictionary.get("directory", "")
		
		if self.revision in (None, ""): self.revision = None
		if self.directory is None: self.directory = ""
		
		return self
	
	def toDictionary(self, out = None):
		if out is None: out = {}
		
		out["id"]           = str(self.id)
		out["repositoryId"] = str(self.repositoryId)
		out["url"]          = self.repository.url
		out["revision"]     = self.revision
		out["directory"]    = self.directory
		
		return out
	
	def lockDirectory(self):
		return self.repository.lockRevision(self)
	
	def unlockDirectory(self):
		return self.repository.unlockRevision()
	
	# Static
	@classmethod
	def validateFormFieldsDictionary(cls, dictionary):
		if dictionary.get("url", "") in (None, ""): return False, { "field": "url", "message": "You must provide a valid repository URL." }
		return True, None
	
	# IRepositoryTree
	@property
	def repositoryUrl(self):
		return self.getRepositoryUrl()
	
	def getRepositoryUrl(self):
		if self.repositoryId is None: return None
		return self.repository.url
	
	def setRepositoryUrl(self, databaseSession, repositoryUrl):
		if self.getRepositoryUrl() == repositoryUrl: return self
		
		self.repositoryClass.setRepository(databaseSession, repositoryUrl, self)
		
		return self
	
	# Static
	@classmethod
	def create(cls, databaseSession, repositoryUrl):
		repositoryTree = cls()
		repositoryTree.repositoryClass.addRef(databaseSession, repositoryUrl, repositoryTree)
		
		return repositoryTree
	
	# RepositoryTree
	# Internal
	@property
	def repositoryClass(self):
		raise NotImplementedError()
