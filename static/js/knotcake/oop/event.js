var Knotcake = Knotcake || {};
Knotcake.OOP = Knotcake.OOP || {};

var self = {};
Knotcake.OOP.Event = Knotcake.OOP.Class(self);

self.ctor = function()
{
	this.callbacks = {};
	this.anonymousCallbacks = [];
};

self.addListener = function(nameOrCallback, callback)
{
	var name = nameOrCallback;
	if (typeof(nameOrCallback) == "function")
	{
		name = null;
		callback = nameOrCallback;
	}
	
	if (name == null)
	{
		this.anonymousCallbacks.push(callback);
	}
	else
	{
		self.callbacks[name] = callback;
	}
};

self.removeListener = function(nameOrCallback)
{
	var name = nameOrCallback;
	var callback = null;
	if (typeof(nameOrCallback) == "function")
	{
		name = null;
		callback = nameOrCallback;
	}
	
	if (name == null)
	{
		var index = this.anonymousCallbacks.indexOf(callback);
		if (index == -1) { return false; }
		
		this.anonymousCallbacks.splice(index, 1);
	}
	else
	{
		if (!self.callbacks[name]) { return false; }
		
		delete self.callbacks[name];
	}
	
	return true;
};

self.dispatch = function()
{
	for (var name in this.callbacks)
	{
		var callback = this.callbacks[name];
		callback.apply(this, arguments);
	}
	
	for (var i in this.anonymousCallbacks)
	{
		var callback = this.anonymousCallbacks[i];
		callback.apply(this, arguments);
	}
};
