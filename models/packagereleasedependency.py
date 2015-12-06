from sqlalchemy import select, func
from sqlalchemy import Column, PrimaryKeyConstraint, ForeignKey, UniqueConstraint
from sqlalchemy import Boolean, Integer, BigInteger, Text
from sqlalchemy import Enum
from sqlalchemy.orm import relationship, column_property, reconstructor

from base import Base

class PackageReleaseDependency(Base):
	__tablename__ = "package_release_dependency"
	
	id               = Column("id",                 BigInteger, nullable = False)
	packageReleaseId = Column("package_release_id", BigInteger, ForeignKey("package_releases.id"), nullable = False)
	repositoryUrl    = Column("repository_url",     Text,       nullable = True)
	name             = Column("name",               Text,       nullable = False)
	versionTimestamp = Column("version_timestamp",  BigInteger, nullable = False)
	
	packageRelease   = relationship("PackageRelease", uselist = False)
	
	PrimaryKeyConstraint(id)
