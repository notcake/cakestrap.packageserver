var self = {};
var ResultState = Knotcake.OOP.Class(self);

self.ctor = function()
{
	this.state   = "none";
	this.message = null;
	
	this.changed = new Knotcake.OOP.Event();
};

self.getState = function()
{
	return this.state;
};

self.getMessage = function()
{
	return this.message;
};

self.isNone    = function() { return this.state == "none";    }
self.isPending = function() { return this.state == "pending"; }
self.isSuccess = function() { return this.state == "success"; }
self.isFailure = function() { return this.state == "failure"; }

self.none    = function(message) { this.state = "none";    this.message = message; this.changed.dispatch(this.state, this.message); };
self.pending = function(message) { this.state = "pending"; this.message = message; this.changed.dispatch(this.state, this.message); };
self.success = function(message) { this.state = "success"; this.message = message; this.changed.dispatch(this.state, this.message); };
self.failure = function(message) { this.state = "failure"; this.message = message; this.changed.dispatch(this.state, this.message); };

self.toVisibility = function()
{
	if (this.state == "none") { return false; }
	return true;
};

self.toClassName = function()
{
	if (this.state == "success") { return "has-success"; }
	else if (this.state == "failure") { return "has-error"; }
	return "";
};

self.toIcon = function()
{
	if (this.state == "none") { return null; }
	else if (this.state == "pending") { return "spinner"; }
	else if (this.state == "success") { return "tick"; }
	else if (this.state == "failure") { return "cross"; }
};
