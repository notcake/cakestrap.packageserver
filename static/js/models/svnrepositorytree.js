var self = {};
var SvnRepositoryTree = Knotcake.OOP.Class(self)

self.ctor = function(svnRepositoryTreeInformation)
{
	this.id              = null;
	this.svnRepositoryId = null;
	this.url             = null;
	this.revision        = null;
	this.directory       = null;
	
	for (var k in svnRepositoryTreeInformation)
	{
		this[k] = svnRepositoryTreeInformation[k];
	}
};
