import os.path
import re
import subprocess

from sqlalchemy import select, func
from sqlalchemy import Column, PrimaryKeyConstraint, ForeignKey, UniqueConstraint
from sqlalchemy import Boolean, Integer, BigInteger, Text
from sqlalchemy import Enum
from sqlalchemy.orm import relationship, column_property

import knotcake.concurrency

from base import Base

class GitRepository(Base):
	__tablename__                 = "git_repositories"
	
	id                            = Column("id",             BigInteger, nullable = False)
	url                           = Column("url",            Text,       nullable = False)
	directoryName                 = Column("directory_name", Text,       nullable = False)
	
	packageGitRepositories        = relationship("PackageGitRepository",        uselist = True)
	packageReleaseGitRepositories = relationship("PackageReleaseGitRepository", uselist = True)
	
	PrimaryKeyConstraint(id)
	UniqueConstraint(url)
	UniqueConstraint(directoryName)
	
	repositoryDirectoryPath = None
	repositoryDirectoryLock = None
	
	def __init__(self):
		super(GitRepository, self).__init__()
		
		self.repositoryLock = None
	
	def initialize(self):
		self.lock()
		subprocess.call(["git", "clone", self.url, self.getFullPath()], env = { "GIT_TERMINAL_PROMPT": "0" })
		self.unlock()
	
	def getFullPath(self):
		return os.path.join(self.getRepositoryDirectoryPath(), self.directoryName)
	
	def generateDirectoryName(self, databaseSession):
		baseDirectoryName = re.sub(r"/[^:@]*(:[^@]*)?@", u"/", self.url)
		baseDirectoryName = re.sub(r"[^a-zA-Z0-9\.]+", u"_", baseDirectoryName)
		baseDirectoryName = baseDirectoryName.lower()
		if self.isDirectoryNameFree(databaseSession, baseDirectoryName):
			self.directoryName = baseDirectoryName
			return self.directoryName
		
		n = 2
		while not self.isDirectoryNameFree(databaseSession, baseDirectoryName + u"_" + unicode(n)):
			n += 1
		
		self.directoryName = baseDirectoryName + u"_" + unicode(n)
		return self.directoryName
	
	def lock(self):
		if self.repositoryLock is None:
			lockPath = self.getFullPath() + ".lock"
			self.repositoryLock = knotcake.concurrency.FileLock(lockPath)
		
		self.repositoryLock.lock()
	
	def unlock(self):
		self.repositoryLock.unlock()
	
	@classmethod
	def addRef(cls, databaseSession, repositoryUrl, gitRepositoryDerivative):
		databaseSession.commit()
		
		cls.lockRepositoryDirectory()
		gitRepositoryDerivative.gitRepository = cls.create(databaseSession, repositoryUrl)
		databaseSession.commit()
		cls.unlockRepositoryDirectory()
	
	@classmethod
	def release(cls, databaseSession, gitRepositoryDerivative):
		databaseSession.commit()
		
		cls.lockRepositoryDirectory()
		databaseSession.delete(gitRepositoryDerivative)
		databaseSession.commit()
		cls.unlockRepositoryDirectory()
	
	@classmethod
	def getRepositoryDirectoryPath(cls):
		if cls.repositoryDirectoryPath is None:
			cls.repositoryDirectoryPath = os.path.join(__file__, "../../data/git")
			cls.repositoryDirectoryPath = os.path.normpath(cls.repositoryDirectoryPath)
			if not os.path.exists(cls.repositoryDirectoryPath):
				os.makedirs(cls.repositoryDirectoryPath)
			print(cls.repositoryDirectoryPath)
		
		return cls.repositoryDirectoryPath
	
	@classmethod
	def getByUrl(cls, databaseSession, url):
		gitRepository = databaseSession.query(cls).filter(cls.url == url).first()
		return gitRepository
	
	@classmethod
	def getByDirectoryName(cls, databaseSession, directoryName):
		gitRepository = databaseSession.query(cls).filter(cls.directoryName == directoryName).first()
		return gitRepository
	
	@classmethod
	def isDirectoryNameFree(cls, databaseSession, directoryName):
		if directoryName == "": return False
		if directoryName == "git": return False
		if directoryName == "git.lock": return False
		
		if cls.getByDirectoryName(databaseSession, directoryName) is not None: return False
		if cls.getByDirectoryName(databaseSession, directoryName + ".lock") is not None: return False
		if directoryName.endswith(".lock"):
			if cls.getByDirectoryName(databaseSession, directoryName[:-len(".lock")]) is not None: return False
		
		return True
	
	@classmethod
	def create(cls, databaseSession, url):
		cls.lockRepositoryDirectory()
		gitRepository = cls.getByUrl(databaseSession, url)
		if gitRepository: return gitRepository
		
		gitRepository = GitRepository()
		gitRepository.url = url
		gitRepository.generateDirectoryName(databaseSession)
		
		gitRepository.initialize()
		
		databaseSession.add(gitRepository)
		databaseSession.commit()
		cls.unlockRepositoryDirectory()
		
		return gitRepository
	
	@classmethod
	def lockRepositoryDirectory(cls):
		if cls.repositoryDirectoryLock is None:
			lockPath = os.path.join(cls.getRepositoryDirectoryPath(), "git.lock")
			print(lockPath)
			cls.repositoryDirectoryLock = knotcake.concurrency.FileLock(lockPath)
		
		cls.repositoryDirectoryLock.lock()
	
	@classmethod
	def unlockRepositoryDirectory(cls):
		cls.repositoryDirectoryLock.unlock()
