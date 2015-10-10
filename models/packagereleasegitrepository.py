from sqlalchemy import select, func
from sqlalchemy import Column, PrimaryKeyConstraint, ForeignKey, UniqueConstraint
from sqlalchemy import Boolean, Integer, BigInteger, Text
from sqlalchemy import Enum
from sqlalchemy.orm import relationship, column_property

from base import Base

class PackageReleaseGitRepository(Base):
	__tablename__    = "package_release_git_repositories"
	
	packageReleaseId = Column("package_release_id", BigInteger, ForeignKey("package_releases.id"), nullable = False)
	gitRepositoryId  = Column("git_repository_id",  BigInteger, ForeignKey("git_repositories.id"), nullable = False)
	branch           = Column("branch",             Text,       nullable = False)
	revision         = Column("revision",           Text,       nullable = True)
	
	packageRelease   = relationship("PackageRelease", uselist = False)
	gitRepository    = relationship("GitRepository",  uselist = False)
	
	PrimaryKeyConstraint(packageReleaseId)
