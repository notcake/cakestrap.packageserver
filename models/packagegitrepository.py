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
	
	package         = relationship("Package",       uselist = False)
	gitRepository   = relationship("GitRepository", uselist = False)
	
	PrimaryKeyConstraint(packageId)
