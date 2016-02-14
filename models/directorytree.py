from sqlalchemy import select, func
from sqlalchemy import Column, PrimaryKeyConstraint, ForeignKey, UniqueConstraint
from sqlalchemy import Boolean, Integer, BigInteger, Text
from sqlalchemy import Enum
from sqlalchemy.orm import relationship, column_property, reconstructor

from knotcake.oop import instance

from idirectorytree import IDirectoryTree

class DirectoryTree(IDirectoryTree):
	__tablename__   = "directory_trees"
	
	id                  = Column("id",                     BigInteger, nullable = False)
	type                = Column("type",                   Enum("svn", "git", "raw"), nullable = False)
	svnRepositoryTreeId = Column("svn_repository_tree_id", BigInteger, ForeignKey("svn_repository_trees.id"), nullable = True)
	gitRepositoryTreeId = Column("git_repository_tree_id", BigInteger, ForeignKey("git_repository_trees.id"), nullable = True)
	rawDirectoryTreeId  = Column("raw_directory_tree_id",  BigInteger, nullable = True)
	
	svnRepositoryTree   = relationship("SvnRepositoryTree", uselist = False, single_parent = True, lazy = "joined", cascade = "save-update, delete, delete-orphan")
	gitRepositoryTree   = relationship("GitRepositoryTree", uselist = False, single_parent = True, lazy = "joined", cascade = "save-update, delete, delete-orphan")
	# rawDirectoryTree    = relationship("RawDirectoryTree",  uselist = False, single_parent = True, lazy = "joined", cascade = "save-update, delete, delete-orphan")
	rawDirectoryTree    = None
	
	PrimaryKeyConstraint(id)
	
	# IDirectoryTree
	def clone(self, clone):
		if clone is None: clone = type(self)()
		
		clone.copy(self)
		return clone
	
	def copy(self, source):
		self.clear()
		self.type = source.type
		if source.directoryTree is not None:
			self.directoryTree = source.directoryTree.clone()
		
		return self
	
	def createPermalink(self):
		permalink = type(self)()
		permalink.type = self.type
		
		if self.directoryTree is not None:
			permalink.directoryTree = self.directoryTree.createPermalink()
		
		return permalink
	
	@property
	def garbageCollectable(self):
		directoryTree = self.directoryTree
		if directoryTree is None: return None
		return directoryTree.garbageCollectable
	
	@instance
	def equals(a, b):
		if a == b: return True
		if type(a) != type(b): return False
		
		if a.type != b.type: return False
		if a.directoryTree == b.directoryTree: return True
		
		if a.directoryTree is not None:
			return a.directoryTree.equals(b.directoryTree)
		else:
			return False
	
	def remove(self, databaseSession):
		databaseSession.delete(self)
		self.clear(databaseSession)
	
	def fromFormFieldsDictionary(self, databaseSession, dictionary):
		from svnrepositorytree import SvnRepositoryTree
		from gitrepositorytree import GitRepositoryTree
		
		if dictionary["type"] == "none":
			self.setNone(databaseSession)
		elif dictionary["type"] == "svn":
			repositoryUrl = dictionary["url"]
			svnRepositoryTree = SvnRepositoryTree()
			svnRepositoryTree.fromFormFieldsDictionary(databaseSession, dictionary)
			self.setSvnRepositoryTree(databaseSession, repositoryUrl, svnRepositoryTree)
		elif dictionary["type"] == "git":
			repositoryUrl = dictionary["url"]
			gitRepositoryTree = GitRepositoryTree()
			gitRepositoryTree.fromFormFieldsDictionary(databaseSession, dictionary)
			self.setGitRepositoryTree(databaseSession, repositoryUrl, gitRepositoryTree)
		elif dictionary["type"] == "raw":
			raise NotImplementedError()
		else:
			raise ValueError()
		
		return self
	
	def toDictionary(self, out = None):
		if out is None: out = {}
		
		if self.type == "svn":   out = self.svnRepositoryTree.toDictionary(out)
		elif self.type == "git": out = self.gitRepositoryTree.toDictionary(out)
		elif self.type == "raw": out = self.rawDirectoryTree.toDictionary(out)
		
		out["type"]                = self.type
		out["svnRepositoryTreeId"] = str(self.svnRepositoryTreeId)
		out["gitRepositoryTreeId"] = str(self.gitRepositoryTreeId)
		out["rawDirectoryTreeId"]  = str(self.rawDirectoryTreeId)
		
		return out
	
	def lockDirectory(self):
		if self.directoryTree is None: return None
		return self.directoryTree.lock()
	
	def unlockDirectory(self):
		if self.directoryTree is None: return None
		return self.directoryTree.lock()
	
	# Static
	@classmethod
	def validateFormFieldsDictionary(cls, dictionary):
		from svnrepositorytree import SvnRepositoryTree
		from gitrepositorytree import GitRepositoryTree
		
		type = dictionary.get("type", "")
		
		if type == "none": return True, None
		elif type == "svn": return SvnRepositoryTree.validateFormFieldsDictionary(dictionary)
		elif type == "git": return GitRepositoryTree.validateFormFieldsDictionary(dictionary)
		elif type == "raw": return RawDirectoryTree.validateFormFieldsDictionary(dictionary)
		else: return False, { "field": "type", "message": "You must provide a valid directory tree type." }
	
	# DirectoryTree
	@property
	def directoryTree(self):
		if self.type   == "svn": return self.svnRepositoryTree
		elif self.type == "git": return self.gitRepositoryTree
		elif self.type == "raw": return self.rawDirectoryTree
		return None
	
	def clear(self, databaseSession):
		if self.directoryTree is None: return
		
		directoryTree = self.directoryTree
		self.directoryTree = None
		databaseSession.delete(directoryTree)
		
		directoryTree.remove(databaseSession)
	
	def setDirectoryTree(self, databaseSession, type, *args):
		if type == "none": self.setNone(databaseSession)
		elif type == "svn": self.setSvnRepositoryTree(databaseSession, *args)
		elif type == "git": self.setGitRepositoryTree(databaseSession, *args)
		elif type == "raw": self.setRawDirectoryTree(databaseSession, *args)
		else: raise NotImplementedError()
	
	def setNone(self, databaseSession):
		self.setType(databaseSession, "none")
	
	def setSvnRepositoryTree(self, databaseSession, repositoryUrl, sourceSvnRepositoryTree):
		from svnrepositorytree import SvnRepositoryTree
		
		destinationSvnRepositoryTree = self.svnRepositoryTree
		if destinationSvnRepositoryTree is None: destinationSvnRepositoryTree = SvnRepositoryTree()
		
		destinationSvnRepositoryTree.copy(sourceSvnRepositoryTree)
		destinationSvnRepositoryTree.setRepositoryUrl(databaseSession, repositoryUrl)
		
		self.setType(databaseSession, "svn")
		if self.svnRepositoryTree is None:
			self.svnRepositoryTree = destinationSvnRepositoryTree
			databaseSession.add(self.svnRepositoryTree)
	
	def setGitRepositoryTree(self, databaseSession, repositoryUrl, sourceGitRepositoryTree):
		from gitrepositorytree import GitRepositoryTree
		
		destinationGitRepositoryTree = self.gitRepositoryTree
		if destinationGitRepositoryTree is None: destinationGitRepositoryTree = GitRepositoryTree()
		
		destinationGitRepositoryTree.copy(sourceGitRepositoryTree)
		destinationGitRepositoryTree.setRepositoryUrl(databaseSession, repositoryUrl)
		
		self.setType(databaseSession, "git")
		if self.gitRepositoryTree is None:
			self.gitRepositoryTree = destinationGitRepositoryTree
			databaseSession.add(self.gitRepositoryTree)
	
	def toDictionaryRecursive(self, out = None):
		return self.toDictionary(out)
	
	# Internal
	@directoryTree.setter
	def directoryTree(self, directoryTree):
		if self.type   == "svn": self.svnRepositoryTree = directoryTree
		elif self.type == "git": self.gitRepositoryTree = directoryTree
		elif self.type == "raw": self.rawDirectoryTree  = directoryTree
	
	def setType(self, databaseSession, type):
		if self.type == type: return self
		
		self.clear(databaseSession)
		self.type = type
		
		return self
	
	# Static
	@classmethod
	def create(cls, databaseSession, type, *args):
		directoryTree = cls()
		directoryTree.setDirectoryTree(databaseSession, type, *args)
		return directoryTree
	
	@classmethod
	def set(cls, directoryTree, databaseSession, type, *args):
		if type in (None, "none"):
			if directoryTree is None: return None
			
			directoryTree.remove(databaseSession)
			directoryTree = None
		elif directoryTree is None:
			directoryTree = cls()
			directoryTree.setDirectoryTree(databaseSession, type, *args)
			
			databaseSession.add(directoryTree)
		else:
			directoryTree.setDirectoryTree(databaseSession, type, *args)
		
		return directoryTree
	
	@classmethod
	def setFromFormFieldsDictionary(cls, directoryTree, databaseSession, dictionary):
		if dictionary.get("type", "none") == "none":
			if directoryTree is None: return None
			
			directoryTree.remove(databaseSession)
			directoryTree = None
		elif directoryTree is None:
			directoryTree = cls()
			directoryTree.fromFormFieldsDictionary(databaseSession, dictionary)
			
			databaseSession.add(directoryTree)
		else:
			directoryTree.fromFormFieldsDictionary(databaseSession, dictionary)
		
		return directoryTree
