var self = {};
var GitRepositoryTree = Knotcake.OOP.Class(self);

self.ctor = function(gitRepositoryTreeInformation)
{
	this.id              = null;
	this.gitRepositoryId = null;
	this.url             = null;
	this.branch          = null;
	this.revision        = null;
	this.directory       = null;
	
	for (var k in gitRepositoryTreeInformation)
	{
		this[k] = gitRepositoryTreeInformation[k];
	}
};
