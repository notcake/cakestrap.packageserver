var self = {};
var User = Knotcake.OOP.Class(self)

var RankIcons = {
	user:          "/static/images/silkicons/user.png",
	moderator:     "/static/images/silkicons/shield.png",
	administrator: "/static/images/silkicons/shield.png",
	overlord:      "/static/images/steam/emoticons/roar.png"
};

var RankNames = {
	user:          "Peasant Scrub",
	moderator:     "Moderator",
	administrator: "Thought Police",
	overlord:      "Reptilian Overlord"
};

self.ctor = function(userInformation)
{
	this.id                      = null;
	this.steamId64               = null;
	this.displayName             = "Nobody";
	this.smallProfilePictureUrl  = "https://steamcdn-a.akamaihd.net/steamcommunity/public/images/avatars/fe/fef49e7fa7e1997310d705b2a6158ff8dc1cdfeb.jpg";
	this.mediumProfilePictureUrl = "https://steamcdn-a.akamaihd.net/steamcommunity/public/images/avatars/fe/fef49e7fa7e1997310d705b2a6158ff8dc1cdfeb_medium.jpg";
	this.largeProfilePictureUrl  = "https://steamcdn-a.akamaihd.net/steamcommunity/public/images/avatars/fe/fef49e7fa7e1997310d705b2a6158ff8dc1cdfeb_full.jpg";
	this.rank                    = "user";
	this.creationTimestamp       = 0;
	this.lastLoginTimestamp      = null;
	this.lastActivityTimestamp   = null;
	
	for (var k in userInformation)
	{
		this[k] = userInformation[k];
	}
};

self.getBasePath = function()
{
	return "/users/" + this.steamId64;
};

self.isAnonymous = function()
{
	return this.id == null;
};

self.isModerator = function()
{
	if (this.rank == "moderator")     { return true; }
	if (this.rank == "administrator") { return true; }
	if (this.rank == "overlord")      { return true; }
	return false;
};

self.isAdministrator = function()
{
	if (this.rank == "administrator") { return true; }
	if (this.rank == "overlord")      { return true; }
	return false;
};

self.isOverlord = function()
{
	if (this.rank == "overlord")      { return true; }
	return false;
};

self.canCreatePackages = function()
{
	return this.isModerator();
};

self.canEditPackages = function()
{
	return this.isModerator();
};

self.canEditPackage = function(package)
{
	return this.isModerator() || package.creatorUserId == this.id;
};

self.canDeletePackages = function()
{
	return this.isAdministrator();
};

self.canDeletePackage = function(package)
{
	return this.isAdministrator();
};

self.canCreatePackageRelease = function(package)
{
	return this.canEditPackage(package);
}

self.canDeletePackageRelease = function(package, packageRelease)
{
	return this.canEditPackage(package);
}

self.getRankIcon = function()
{
	return RankIcons[this.rank];
};

self.getRankName = function()
{
	return RankNames[this.rank];
};
