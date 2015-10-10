from sqlalchemy import select, func
from sqlalchemy import Column, PrimaryKeyConstraint, ForeignKey, UniqueConstraint
from sqlalchemy import Boolean, Integer, BigInteger, Text
from sqlalchemy import Enum
from sqlalchemy.orm import relationship, column_property

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
