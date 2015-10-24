var self = {};
var PackageGitRepository = Knotcake.OOP.Class(self)

self.ctor = function(packageGitRepositoryInformation)
{
	this.packageId = null;
	this.url       = null;
	this.branch    = null;
	this.revision  = null;
	this.directory = null;
	
	for (var k in packageGitRepositoryInformation)
	{
		this[k] = packageGitRepositoryInformation[k];
	}
};
