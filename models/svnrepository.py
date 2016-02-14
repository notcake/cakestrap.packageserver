import os.path
import subprocess

from sqlalchemy import select, func
from sqlalchemy import Column, PrimaryKeyConstraint, ForeignKey, UniqueConstraint
from sqlalchemy import Boolean, Integer, BigInteger, Text
from sqlalchemy import Enum
from sqlalchemy.orm import relationship, column_property, reconstructor

import knotcake.concurrency

from repository import Repository

class SvnRepository(Repository):
	__tablename__   = "svn_repositories"
	
	id              = Column("id",             BigInteger, nullable = False)
	url             = Column("url",            Text,       nullable = False)
	directoryName   = Column("directory_name", Text,       nullable = False)
	
	repositoryTrees = relationship("SvnRepositoryTree", uselist = True)
	
	PrimaryKeyConstraint(id)
	UniqueConstraint(url)
	UniqueConstraint(directoryName)
	
	repositoryDirectoryName     = "svn"
	repositoryDirectoryLockName = "svn"
	
	def __init__(self):
		super(SvnRepository, self).__init__()
		
		self.init()
	
	# IRepository
	def getHeadRevision(self, repositoryTree):
		if not self.lockDirectory(): return None
		
		revision = subprocess.check_output(["svnversion"], cwd = self.getFullPath())
		
		self.unlockDirectory()
		
		return revision
	
	# Repository
	# Internal
	@property
	def repositoryTreeClass(self):
		from svnrepositorytree import SvnRepositoryTree
		return SvnRepositoryTree
	
	def initialize(self):
		self.repositoryLock.lock()
		subprocess.call(["svn", "clone", self.url, self.getFullPath()], env = { "GIT_TERMINAL_PROMPT": "0" })
		self.repositoryLock.unlock()
	
	def uninitialize(self):
		if self.lockDirectory():
			if self.directoryExists():
				subprocess.call(["rm", "-rf", self.getFullPath()])
			self.unlockDirectory()
		
		self.repositoryLock.delete()
	
	def directoryExists(self):
		return os.path.exists(os.path.join(self.getFullPath(), ".svn"))
	
	# SvnRepository
	def lockRevision(self, gitRepositoryTree):
		directoryPath = os.path.normpath(gitRepositoryTree.directory)
		if directoryPath.startswith("../") or os.path.isabs(directoryPath):
			return None
		
		repositoryPath = self.getFullPath()
		
		if not self.lockDirectory(): return None
		
		revision = gitRepositoryTree.revision
		if revision is None: revision = "HEAD"
		
		subprocess.call(["svn", "update", "-r", revision], cwd = repositoryPath)
		
		return os.path.join(repositoryPath, directoryPath)
	
	def unlockRevision(self):
		self.unlockDirectory()
	
	# Internal
	def lockDirectory(self):
		self.getRepositoryDirectoryLock().lock()
		if not self.directoryExists():
			self.getRepositoryDirectoryLock().unlock()
			return False
		
		self.repositoryLock.lock()
		self.getRepositoryDirectoryLock().unlock()
		
		return True
	
	def unlockDirectory(self):
		self.repositoryLock.unlock()
