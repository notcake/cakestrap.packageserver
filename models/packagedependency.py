from sqlalchemy import select, func
from sqlalchemy import Column, PrimaryKeyConstraint, ForeignKey, UniqueConstraint
from sqlalchemy import Boolean, Integer, BigInteger, Text
from sqlalchemy import Enum
from sqlalchemy.orm import relationship, column_property, reconstructor

from base import Base

class PackageDependency(Base):
	__tablename__    = "package_dependency"
	
	id               = Column("id",                BigInteger, nullable = False)
	packageId        = Column("package_id",        BigInteger, ForeignKey("packages.id"), nullable = False)
	repositoryUrl    = Column("repository_url",    Text,       nullable = True)
	name             = Column("name",              Text,       nullable = False)
	versionTimestamp = Column("version_timestamp", BigInteger, nullable = True)
	
	package          = relationship("Package", uselist = False)
	
	PrimaryKeyConstraint(id)
