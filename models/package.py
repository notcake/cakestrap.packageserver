from datetime import datetime
import time

from sqlalchemy import select, func
from sqlalchemy import Column, PrimaryKeyConstraint, ForeignKey, UniqueConstraint
from sqlalchemy import Boolean, Integer, BigInteger, Text
from sqlalchemy import Enum
from sqlalchemy.orm import relationship, column_property, reconstructor

from base import Base

class Package(Base):
	__tablename__            = "packages"
	
	id                       = Column("id",                          BigInteger, nullable = False)
	name                     = Column("name",                        Text,       nullable = False)
	displayName              = Column("display_name",                Text,       nullable = False)
	description              = Column("description",                 Text,       nullable = False)
	codeDirectoryTreeId      = Column("code_directory_tree_id",      BigInteger, ForeignKey("directory_trees.id"), nullable = True)
	resourcesDirectoryTreeId = Column("resources_directory_tree_id", BigInteger, ForeignKey("directory_trees.id"), nullable = True)
	creatorUserId            = Column("creator_user_id",             BigInteger, ForeignKey("users.id"),           nullable = False)
	
	codeDirectoryTree        = relationship("DirectoryTree",        uselist = False, single_parent = True, cascade = "save-update, delete", foreign_keys = [codeDirectoryTreeId])
	resourcesDirectoryTree   = relationship("DirectoryTree",        uselist = False, single_parent = True, cascade = "save-update, delete", foreign_keys = [resourcesDirectoryTreeId])
	creatorUser              = relationship("User",                 uselist = False)
	dependencies             = relationship("PackageDependency",    uselist = True,  cascade = "delete")
	releases                 = relationship("PackageRelease",       uselist = True,  cascade = "delete", order_by="desc(PackageRelease.versionTimestamp)")
	
	PrimaryKeyConstraint(id)
	
	def createRelease(self, databaseSession, timestamp):
		from pathutils      import PathUtils
		from packagerelease import PackageRelease
		from directorytree  import DirectoryTree
		
		codeDirectoryTree      = None
		resourcesDirectoryTree = None
		if self.codeDirectoryTree is not None:
			codeDirectoryTree = self.codeDirectoryTree.createPermalink()
		if self.resourcesDirectoryTree is not None:
			resourcesDirectoryTree = self.resourcesDirectoryTree.createPermalink()
		
		latestPackage = self.getLatestPackageRelease(databaseSession)
		if (latestPackage and
		    DirectoryTree.equals(latestPackage.codeDirectoryTree, codeDirectoryTree) and
		    DirectoryTree.equals(latestPackage.resourcesDirectoryTree, resourcesDirectoryTree)):
			return latestPackage
		
		packageRelease = PackageRelease()
		packageRelease.package                = self
		packageRelease.versionTimestamp       = timestamp
		packageRelease.versionName            = datetime.utcfromtimestamp(timestamp).date().isoformat()
		packageRelease.fileName               = PathUtils.createFileName(self.name) + "-" + packageRelease.versionName
		packageRelease.codeDirectoryTree      = codeDirectoryTree
		packageRelease.resourcesDirectoryTree = resourcesDirectoryTree
		
		databaseSession.add(packageRelease)
		
		return packageRelease
	
	def getLatestPackageRelease(self, databaseSession):
		from packagerelease import PackageRelease
		return databaseSession \
		       .query(PackageRelease) \
		       .filter(PackageRelease.packageId == self.id) \
		       .order_by(PackageRelease.versionTimestamp.desc()) \
		       .first()
	
	def remove(self, databaseSession):
		garbageCollectables = set()
		if self.codeDirectoryTree      is not None: garbageCollectables.add(self.codeDirectoryTree.garbageCollectable)
		if self.resourcesDirectoryTree is not None: garbageCollectables.add(self.resourcesDirectoryTree.garbageCollectable)
		
		for packageRelease in self.releases:
			if packageRelease.codeDirectoryTree      is not None: garbageCollectables.add(packageRelease.codeDirectoryTree.garbageCollectable)
			if packageRelease.resourcesDirectoryTree is not None: garbageCollectables.add(packageRelease.resourcesDirectoryTree.garbageCollectable)
		
		if None in garbageCollectables:
			garbageCollectables.remove(None)
		
		databaseSession.delete(self)
		databaseSession.commit()
		
		for garbageCollectable in garbageCollectables:
			garbageCollectable.gc(databaseSession)
	
	def setCodeDirectoryTree(self, databaseSession, type, *args):
		from directorytree import DirectoryTree
		self.codeDirectoryTree = DirectoryTree.set(self.codeDirectoryTree, databaseSession, type, *args)
	
	def setResourcesDirectoryTree(self, databaseSession, type, *args):
		from directorytree import DirectoryTree
		self.resourcesDirectoryTree = DirectoryTree.set(self.resourcesDirectoryTree, databaseSession, type, *args)
	
	def setCodeDirectoryTreeFromFormFieldsDictionary(self, databaseSession, dictionary):
		from directorytree import DirectoryTree
		self.codeDirectoryTree = DirectoryTree.setFromFormFieldsDictionary(self.codeDirectoryTree, databaseSession, dictionary)
	
	def setResourcesDirectoryTreeFromFormFieldsDictionary(self, databaseSession, dictionary):
		from directorytree import DirectoryTree
		self.resourcesDirectoryTree = DirectoryTree.setFromFormFieldsDictionary(self.resourcesDirectoryTree, databaseSession, dictionary)
	
	def fromFormFieldsDictionary(self, databaseSession, dictionary):
		self.name        = dictionary.get("name",        "")
		self.displayName = dictionary.get("displayName", "")
		self.description = dictionary.get("description", "")
		
		if self.displayName in (None, ""): self.displayName = self.name
		
		return self
	
	def toDictionary(self, out = None):
		if out is None: out = {}
		
		out["id"]            = str(self.id)
		out["name"]          = self.name
		out["displayName"]   = self.displayName
		out["description"]   = self.description
		out["creatorUserId"] = self.creatorUserId
		
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
	
	@classmethod
	def getByName(cls, databaseSession, name):
		name = name.lower()
		package = databaseSession.query(cls).filter(func.lower(cls.name) == name).first()
		return package
	
	@classmethod
	def validateFormFieldsDictionary(cls, dictionary):
		if dictionary.get("name",        "") in (None, ""): return False, { "field": "name",        "message": "You must provide a package name!" }
		if dictionary.get("description", "") in (None, ""): return False, { "field": "description", "message": "You must provide a description!"  }
		
		return True, None
	
	@classmethod
	def validateDirectoryTreeFormFieldsDictionary(cls, dictionary):
		from directorytree import DirectoryTree
		return DirectoryTree.validateFormFieldsDictionary(dictionary)
