from sqlalchemy import select, func
from sqlalchemy import Column, PrimaryKeyConstraint, ForeignKey, UniqueConstraint
from sqlalchemy import Boolean, Integer, BigInteger, Text
from sqlalchemy import Enum
from sqlalchemy.orm import relationship, column_property, reconstructor

from repositorytree import RepositoryTree

class SvnRepositoryTree(RepositoryTree):
	__tablename__ = "svn_repository_trees"
	
	id            = Column("id",            BigInteger, nullable = False)
	repositoryId  = Column("repository_id", BigInteger, ForeignKey("svn_repositories.id"), nullable = False)
	revision      = Column("revision",      Text,       nullable = True)
	directory     = Column("directory",     Text,       nullable = False)
	
	repository    = relationship("SvnRepository", uselist = False, lazy = "joined")
	
	PrimaryKeyConstraint(id)
	
	# IDirectoryTree
	def fromFormFieldsDictionary(self, databaseSession, dictionary):
		super(SvnRepositoryTree, self).fromFormFieldsDictionary(databaseSession, dictionary)
		
		self.directory = dictionary.get("directory", "")
		
		if self.directory is None: self.directory = ""
		if self.directory == "": self.directory = "trunk"
		
		return self
	
	# RepositoryTree
	# Internal
	@property
	def repositoryClass(self):
		from svnrepository import SvnRepository
		return SvnRepository
