from sqlalchemy import select, func
from sqlalchemy import Column, PrimaryKeyConstraint, ForeignKey, UniqueConstraint
from sqlalchemy import Boolean, Integer, BigInteger, Text
from sqlalchemy import Enum
from sqlalchemy.orm import relationship, column_property, reconstructor

from knotcake.oop import instance

from repositorytree import RepositoryTree

class GitRepositoryTree(RepositoryTree):
	__tablename__ = "git_repository_trees"
	
	id            = Column("id",            BigInteger, nullable = False)
	repositoryId  = Column("repository_id", BigInteger, ForeignKey("git_repositories.id"), nullable = False)
	branch        = Column("branch",        Text,       nullable = False)
	revision      = Column("revision",      Text,       nullable = True)
	directory     = Column("directory",     Text,       nullable = False)
	
	repository    = relationship("GitRepository", uselist = False, lazy = "joined")
	
	PrimaryKeyConstraint(id)
	
	# IDirectoryTree
	def copy(self, source):
		super(GitRepositoryTree, self).copy(source)
		
		self.branch = source.branch
		
		return self
	
	@instance
	def equals(a, b):
		if a == b: return True
		if not super(GitRepositoryTree, a).equals(b): return False
		
		if a.branch != b.branch: return False
		
		return True
	
	def fromFormFieldsDictionary(self, databaseSession, dictionary):
		super(GitRepositoryTree, self).fromFormFieldsDictionary(databaseSession, dictionary)
		
		self.branch = dictionary.get("branch", "")
		
		if self.branch in (None, ""): self.branch = "master"
		
		return self
	
	def toDictionary(self, out = None):
		out = super(GitRepositoryTree, self).toDictionary(out)
		
		out["branch"] = self.branch
		
		return out
	
	# RepositoryTree
	# Internal
	@property
	def repositoryClass(self):
		from gitrepository import GitRepository
		return GitRepository
