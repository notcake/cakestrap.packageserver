var self = {};
var DirectoryTree = Knotcake.OOP.Class(self)

self.ctor = function(directoryTreeInformation)
{
	this.id                  = null;
	this.type                = "none";
	this.svnRepositoryTreeId = null;
	this.gitRepositoryTreeId = null;
	this.rawDirectoryTreeId  = null;
	
	this.svnRepositoryTree   = null;
	this.gitRepositoryTree   = null;
	this.rawDirectoryTree    = null;
	
	for (var k in directoryTreeInformation)
	{
		this[k] = directoryTreeInformation[k];
	}
	
	if (this.svnRepositoryTree) {
		this.svnRepositoryTree = new SvnRepositoryTree(this.svnRepositoryTree);
	}
	if (this.gitRepositoryTree) {
		this.gitRepositoryTree = new GitRepositoryTree(this.gitRepositoryTree);
	}
	if (this.rawDirectoryTree) {
		this.rawDirectoryTree = new RawDirectoryTree(this.rawDirectoryTree);
	}
};
