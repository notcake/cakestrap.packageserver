from sqlalchemy import select, func
from sqlalchemy import Column, PrimaryKeyConstraint, ForeignKey, UniqueConstraint
from sqlalchemy import Boolean, Integer, BigInteger, Text
from sqlalchemy import Enum
from sqlalchemy.orm import relationship, column_property, reconstructor

from base import Base

class PackageRelease(Base):
	__tablename__    = "package_releases"
	
	id               = Column("id",                BigInteger, nullable = False)
	packageId        = Column("package_id",        BigInteger, ForeignKey("packages.id"), nullable = False)
	versionTimestamp = Column("version_timestamp", BigInteger, nullable = False)
	versionName      = Column("version_name",      Text,       nullable = False)
	fileName         = Column("file_name",         Text,       nullable = False)
	
	package          = relationship("Package",                     uselist = False)
	gitRepository    = relationship("PackageReleaseGitRepository", uselist = False, cascade="delete")
	dependencies     = relationship("PackageReleaseDependency",    uselist = True,  cascade="delete")
	
	PrimaryKeyConstraint(id)
	UniqueConstraint(packageId, versionTimestamp)
