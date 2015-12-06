from sqlalchemy import select, func
from sqlalchemy import Column, PrimaryKeyConstraint, ForeignKey, UniqueConstraint
from sqlalchemy import Boolean, Integer, BigInteger, Text
from sqlalchemy import Enum
from sqlalchemy.orm import relationship, column_property

from base import Base

class PackageGitRepository(Base):
	__tablename__   = "package_git_repositories"
	
	packageId       = Column("package_id",        BigInteger, ForeignKey("packages.id"),         nullable = False)
	gitRepositoryId = Column("git_repository_id", BigInteger, ForeignKey("git_repositories.id"), nullable = False)
	branch          = Column("branch",            Text,       nullable = False)
	revision        = Column("revision",          Text,       nullable = True)
	directory       = Column("directory",         Text,       nullable = False)
	
	package         = relationship("Package",       uselist = False)
	gitRepository   = relationship("GitRepository", uselist = False, lazy = "joined")
	
	PrimaryKeyConstraint(packageId)
	
	def remove(self, databaseSession):
		from gitrepository import GitRepository
		gitRepository = self.gitRepository
		GitRepository.release(databaseSession, self)
		gitRepository.gc(databaseSession)
	
	def toDictionary(self, out = None):
		if out is None: out = {}
		
		out["packageId"]       = str(self.packageId)
		out["gitRepositoryId"] = str(self.gitRepositoryId)
		out["url"]             = self.gitRepository.url
		out["branch"]          = self.branch
		out["revision"]        = self.revision
		out["directory"]       = self.directory
		
		return out
	
	@classmethod
	def getAll(cls, databaseSession):
		packageGitRepositories = databaseSession.query(cls).order_by(cls.id.desc()).all()
		return packages
	
	@classmethod
	def getByPackage(cls, databaseSession, packageId):
		if isinstance(packageId, Base): packageId = packageId.id
		if packageId is None: return None
		
		packageGitRepository = databaseSession.query(cls).filter(cls.packageId == packageId).first()
		return packageGitRepository
