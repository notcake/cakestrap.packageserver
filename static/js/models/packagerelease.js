var self = {};
var PackageRelease = Knotcake.OOP.Class(self);

self.ctor = function(packageReleaseInformation)
{
	this.id                       = null;
	this.packageId                = null;
	this.versionTimestamp         = null;
	this.versionName              = null;
	this.fileName                 = null;
	this.codeDirectoryTreeId      = null;
	this.resourcesDirectoryTreeId = null;
	
	this.codeDirectoryTree        = null;
	this.resourcesDirectoryTree   = null;
	
	for (var k in packageReleaseInformation)
	{
		this[k] = packageReleaseInformation[k];
	}
	
	if (this.codeDirectoryTree) {
		this.codeDirectoryTree = new DirectoryTree(this.codeDirectoryTree);
	}
	if (this.resourcesDirectoryTree) {
		this.resourcesDirectoryTree = new DirectoryTree(this.resourcesDirectoryTree);
	}
};

self.getBasePath = function()
{
	return "/packages/" + this.packageId + "/releases/" + this.id;
};
