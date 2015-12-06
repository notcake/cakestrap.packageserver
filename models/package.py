from sqlalchemy import select, func
from sqlalchemy import Column, PrimaryKeyConstraint, ForeignKey, UniqueConstraint
from sqlalchemy import Boolean, Integer, BigInteger, Text
from sqlalchemy import Enum
from sqlalchemy.orm import relationship, column_property, reconstructor

from base import Base

class Package(Base):
	__tablename__ = "packages"
	
	id            = Column("id",              BigInteger, nullable = False)
	name          = Column("name",            Text,       nullable = False)
	displayName   = Column("display_name",    Text,       nullable = False)
	description   = Column("description",     Text,       nullable = False)
	creatorUserId = Column("creator_user_id", BigInteger, ForeignKey("users.id"), nullable = False)
	
	creatorUser   = relationship("User",                 uselist = False)
	gitRepository = relationship("PackageGitRepository", uselist = False)
	dependencies  = relationship("PackageDependency",    uselist = True)
	releases      = relationship("PackageRelease",       uselist = True)
	
	PrimaryKeyConstraint(id)
	
	def remove(self, databaseSession):
		from gitrepository import GitRepository
		
		gitRepository = None
		if self.gitRepository is not None:
			gitRepository = self.gitRepository.gitRepository
		
		gitRepositories = databaseSession \
			.query(GitRepository) \
			.join(GitRepository.packageReleaseGitRepositories) \
			.join(PackageReleaseGitRepositories.packageRelease) \
			.filter(PackageRelease.package == self)
		
		gitRepository.gc(databaseSession)
		
		for gitRepository in gitRepositories:
			gitRepository.gc(databaseSession)
	
	def toDictionary(self, out = None):
		if out is None: out = {}
		
		out["id"]            = str(self.id)
		out["name"]          = self.name
		out["displayName"]   = self.displayName
		out["description"]   = self.description
		out["creatorUserId"] = self.creatorUserId
		
		return out
	
	@classmethod
	def getAll(cls, databaseSession):
		packages = databaseSession.query(cls).order_by(cls.id.desc()).all()
		return packages
	
	@classmethod
	def getById(cls, databaseSession, id):
		if id is None: return None
		package = databaseSession.query(cls).filter(cls.id == id).first()
		return package
	
	@classmethod
	def getByName(cls, databaseSession, name):
		name = name.lower()
		package = databaseSession.query(cls).filter(func.lower(cls.name) == name).first()
		return package
