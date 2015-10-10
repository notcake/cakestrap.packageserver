from sqlalchemy import select, func
from sqlalchemy import Column, PrimaryKeyConstraint, ForeignKey, UniqueConstraint
from sqlalchemy import Boolean, Integer, BigInteger, Text
from sqlalchemy import Enum
from sqlalchemy.orm import relationship, column_property

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
