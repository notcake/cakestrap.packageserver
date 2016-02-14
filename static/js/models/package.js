var self = {};
var Package = Knotcake.OOP.Class(self)

self.ctor = function(packageInformation)
{
	this.id                       = null;
	this.name                     = null;
	this.displayName              = null;
	this.description              = null;
	this.creatorUserId            = null;
	this.codeDirectoryTreeId      = null;
	this.resourcesDirectoryTreeId = null;
	
	this.codeDirectoryTree        = null;
	this.resourcesDirectoryTree   = null;
	
	for (var k in packageInformation)
	{
		this[k] = packageInformation[k];
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
	return "/packages/" + this.id;
};
