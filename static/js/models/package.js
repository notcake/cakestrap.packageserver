var self = {};
var Package = Knotcake.OOP.Class(self)

self.ctor = function(packageInformation)
{
	this.id            = null;
	this.name          = null;
	this.displayName   = null;
	this.description   = null;
	this.creatorUserId = null;
	
	for (var k in packageInformation)
	{
		this[k] = packageInformation[k];
	}
};
