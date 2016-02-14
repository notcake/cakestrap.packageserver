import os.path

from sqlalchemy import select, func
from sqlalchemy import Column, PrimaryKeyConstraint, ForeignKey, UniqueConstraint
from sqlalchemy import Boolean, Integer, BigInteger, Text
from sqlalchemy import Enum
from sqlalchemy.orm import relationship, column_property, reconstructor

from base import Base

class PackageRelease(Base):
	__tablename__    = "package_releases"
	
	id                       = Column("id",                          BigInteger, nullable = False)
	packageId                = Column("package_id",                  BigInteger, ForeignKey("packages.id"), nullable = False)
	versionTimestamp         = Column("version_timestamp",           BigInteger, nullable = False)
	versionName              = Column("version_name",                Text,       nullable = False)
	fileName                 = Column("file_name",                   Text,       nullable = False)
	codeDirectoryTreeId      = Column("code_directory_tree_id",      BigInteger, ForeignKey("directory_trees.id"), nullable = True)
	resourcesDirectoryTreeId = Column("resources_directory_tree_id", BigInteger, ForeignKey("directory_trees.id"), nullable = True)
	
	package                  = relationship("Package",                  uselist = False)
	codeDirectoryTree        = relationship("DirectoryTree",            uselist = False, lazy = "joined", cascade = "save-update, delete", foreign_keys = [codeDirectoryTreeId])
	resourcesDirectoryTree   = relationship("DirectoryTree",            uselist = False, lazy = "joined", cascade = "save-update, delete", foreign_keys = [resourcesDirectoryTreeId])
	dependencies             = relationship("PackageReleaseDependency", uselist = True,  cascade = "delete")
	
	PrimaryKeyConstraint(id)
	UniqueConstraint(packageId, versionTimestamp)
	
	def generatePackage(self):
		fullFilePath = self.getFullFilePath()
		if os.path.exists(fullFilePath): return fullFilePath
		
		# help what do i put here
		
		return fullFilePath
	
	def remove(self, databaseSession):
		garbageCollectables = set()
		if self.codeDirectoryTree      is not None: garbageCollectables.add(self.codeDirectoryTree.garbageCollectable)
		if self.resourcesDirectoryTree is not None: garbageCollectables.add(self.resourcesDirectoryTree.garbageCollectable)
		
		if None in garbageCollectables:
			garbageCollectables.remove(None)
		
		databaseSession.delete(self)
		databaseSession.commit()
		
		for garbageCollectable in garbageCollectables:
			garbageCollectable.gc(databaseSession)
	
	def toDictionary(self, out = None):
		if out is None: out = {}
		
		out["id"]                       = self.id
		out["packageId"]                = self.packageId
		out["versionTimestamp"]         = self.versionTimestamp
		out["versionName"]              = self.versionName
		out["fileName"]                 = self.fileName
		out["codeDirectoryTreeId"]      = self.codeDirectoryTreeId
		out["resourcesDirectoryTreeId"] = self.resourcesDirectoryTreeId
		
		return out
	
	def toDictionaryRecursive(self, out = None):
		out = self.toDictionary(out)
		
		out["codeDirectoryTree"]      = None
		out["resourcesDirectoryTree"] = None
		
		if self.codeDirectoryTree is not None:
			out["codeDirectoryTree"] = self.codeDirectoryTree.toDictionaryRecursive()
		
		if self.resourcesDirectoryTree is not None:
			out["resourcesDirectoryTree"] = self.resourcesDirectoryTree.toDictionaryRecursive()
		
		return out
	
	# Internal
	def getFullFileName(self):
		from pathutils import PathUtils
		return PathUtils.createFileName(self.package.name) + "-" + self.fileName + ".bin"
	
	def getFullFilePath(self):
		return os.path.join(self.getPackageReleaseDirectory(), self.getFullFileName())
	
	# Static
	# Internal
	@classmethod
	def getPackageReleasesDirectory(cls):
		packageReleasesDirectory = os.path.join(__file__, "../../data/packages")
		packageReleasesDirectory = os.path.normpath(packageReleasesDirectory)
		if not os.path.exists(packageReleasesDirectory):
			os.makedirs(packageReleasesDirectory)
		return packageReleasesDirectory
