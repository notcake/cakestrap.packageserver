import os.path

from sqlalchemy import select, func
from sqlalchemy import Column, PrimaryKeyConstraint, ForeignKey, UniqueConstraint
from sqlalchemy import Boolean, Integer, BigInteger, Text
from sqlalchemy import Enum
from sqlalchemy.orm import relationship, column_property, reconstructor

from sqlalchemy import and_
from sqlalchemy.orm import aliased

import knotcake.packages

from base import Base

class PackageRelease(Base):
	__tablename__    = "package_releases"
	
	id                       = Column("id",                          BigInteger, nullable = False)
	packageId                = Column("package_id",                  BigInteger, ForeignKey("packages.id"), nullable = False)
	versionTimestamp         = Column("version_timestamp",           BigInteger, nullable = False)
	versionName              = Column("version_name",                Text,       nullable = False)
	fileName                 = Column("file_name",                   Text,       nullable = False)
	fileSize                 = Column("file_size",                   BigInteger, nullable = True)
	codeDirectoryTreeId      = Column("code_directory_tree_id",      BigInteger, ForeignKey("directory_trees.id"), nullable = True)
	resourcesDirectoryTreeId = Column("resources_directory_tree_id", BigInteger, ForeignKey("directory_trees.id"), nullable = True)
	
	package                  = relationship("Package",                  uselist = False)
	codeDirectoryTree        = relationship("DirectoryTree",            uselist = False, single_parent = True, cascade = "save-update, delete", foreign_keys = [codeDirectoryTreeId])
	resourcesDirectoryTree   = relationship("DirectoryTree",            uselist = False, single_parent = True, cascade = "save-update, delete", foreign_keys = [resourcesDirectoryTreeId])
	dependencies             = relationship("PackageReleaseDependency", uselist = True,  cascade = "delete")
	
	PrimaryKeyConstraint(id)
	UniqueConstraint(packageId, versionTimestamp)
	
	def generatePackage(self, databaseSession):
		import knotcake.io
		
		fullFilePath = self.getFullFilePath()
		# if os.path.exists(fullFilePath): return fullFilePath
		
		streamWriter = knotcake.io.FileOutStream(open(fullFilePath, "wb"))
		packageRelease = knotcake.packages.PackageRelease(self.package, self)
		
		codeSection      = knotcake.packages.FileSystemSection.fromDirectoryTree(self.codeDirectoryTree, "code")
		resourcesSection = knotcake.packages.FileSystemSection.fromDirectoryTree(self.resourcesDirectoryTree, "resources")
		
		packageRelease.addSection(codeSection,      "code")
		packageRelease.addSection(resourcesSection, "resources")
		
		packageRelease.serialize(streamWriter)
		self.fileSize = streamWriter.size
		streamWriter.close()
		
		return fullFilePath
	
	def getFullFileName(self):
		from pathutils import PathUtils
		return self.fileName + ".bin"
	
	def remove(self, databaseSession):
		self.removeFile(databaseSession)
		
		garbageCollectables = set()
		if self.codeDirectoryTree      is not None: garbageCollectables.add(self.codeDirectoryTree.garbageCollectable)
		if self.resourcesDirectoryTree is not None: garbageCollectables.add(self.resourcesDirectoryTree.garbageCollectable)
		
		if None in garbageCollectables:
			garbageCollectables.remove(None)
		
		databaseSession.delete(self)
		databaseSession.commit()
		
		for garbageCollectable in garbageCollectables:
			garbageCollectable.gc(databaseSession)
	
	def removeFile(self, databaseSession):
		os.remove(self.getFullFileName())
	
	def toDictionary(self, out = None):
		if out is None: out = {}
		
		out["id"]                       = self.id
		out["packageId"]                = self.packageId
		out["versionTimestamp"]         = self.versionTimestamp
		out["versionName"]              = self.versionName
		out["fileName"]                 = self.fileName
		out["fileSize"]                 = self.fileSize
		out["codeDirectoryTreeId"]      = self.codeDirectoryTreeId
		out["resourcesDirectoryTreeId"] = self.resourcesDirectoryTreeId
		
		out["downloadUrl"]              = "/packages/" + str(self.packageId) + "/releases/" + str(self.id) + "/download"
		
		return out
	
	def toDictionaryRecursive(self, showProtectedInformation, out = None):
		out = self.toDictionary(out)
		
		out["codeDirectoryTree"]      = None
		out["resourcesDirectoryTree"] = None
		
		if self.codeDirectoryTree is not None:
			out["codeDirectoryTree"] = self.codeDirectoryTree.toDictionaryRecursive(showProtectedInformation)
		
		if self.resourcesDirectoryTree is not None:
			out["resourcesDirectoryTree"] = self.resourcesDirectoryTree.toDictionaryRecursive(showProtectedInformation)
		
		return out
	
	# Internal
	def getFullFilePath(self):
		return os.path.join(self.getPackageReleasesDirectory(), self.getFullFileName())
	
	# Static
	@classmethod
	def getLatestPackageReleases(cls, databaseSession):
		packageReleases2 = aliased(cls)
		
		subquery = databaseSession.query(
				packageReleases2.packageId.label("package_releases_package_id"), \
				func.max(packageReleases2.versionTimestamp).label("package_releases_max_version_timestamp") \
			) \
			.select_from(packageReleases2) \
			.group_by(packageReleases2.packageId) \
			.subquery()
		
		return databaseSession.query(cls) \
			.select_from(cls) \
			.join(
				subquery, \
				and_( \
					cls.packageId == subquery.c.package_releases_package_id, \
					cls.versionTimestamp == subquery.c.package_releases_max_version_timestamp \
				) \
			) \
			.all()
	
	# Internal
	@classmethod
	def getPackageReleasesDirectory(cls):
		packageReleasesDirectory = os.path.join(__file__, "../../data/packages")
		packageReleasesDirectory = os.path.normpath(packageReleasesDirectory)
		if not os.path.exists(packageReleasesDirectory):
			os.makedirs(packageReleasesDirectory)
		return packageReleasesDirectory
