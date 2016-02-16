from struct import Struct

class PackageReleaseHeader(Struct):
	def __init__(self, package = None, packageRelease = None):
		self.packageName        = ""
		self.packageDisplayName = ""
		self.packageDescription = ""
		
		self.creatorSteamId64   = ""
		
		self.versionTimestamp   = 0
		self.versionName        = ""
		
		if package is not None:
			self.packageName        = package.name
			self.packageDisplayName = package.displayName
			self.packageDescription = package.description
			
			self.creatorSteamId64   = str(package.creatorUser.steamId64)
		
		if packageRelease is not None:
			self.versionTimestamp   = packageRelease.versionTimestamp
			self.versionName        = packageRelease.versionName
	
	def serialize(self, streamWriter):
		super(PackageReleaseHeader, self).serialize(streamWriter)
		
		streamWriter.stringN8(self.packageName)
		streamWriter.stringN8(self.packageDisplayName)
		streamWriter.stringN32(self.packageDescription)
		
		streamWriter.stringN8(self.creatorSteamId64)
		
		streamWriter.uint64(self.versionTimestamp)
		streamWriter.stringN8(self.versionName)
	
	def deserialize(self, streamReader):
		super(PackageReleaseHeader, self).serialize(streamReader)
		
		self.packageName        = streamReader.stringN8()
		self.packageDisplayName = streamReader.stringN8()
		self.packageDescription = streamReader.stringN32()
		
		self.creatorSteamId64   = streamReader.stringN8()
		
		self.versionTimestamp   = streamReader.uint64()
		self.versionName        = streamReader.stringN8()
