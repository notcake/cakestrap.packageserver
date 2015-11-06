var Knotcake = Knotcake || {}
Knotcake.OOP = Knotcake.OOP || {}

var self = {}
Knotcake.OOP.Field = Knotcake.OOP.Class(self)

Knotcake.OOP.Field.NextInstanceId = 0;

self.ctor = function(initialValue, type)
{
	this.instanceId   = Knotcake.OOP.Field.NextInstanceId;
	Knotcake.OOP.Field.NextInstanceId++;
	
	this.name         = null;
	this.description  = null;
	this.initialValue = initialValue;
	this.nullable     = false;
	this.type         = type;
	
	this.properties   = {};
};

self.getInstanceId = function()
{
	return this.instanceId;
};

self.getName = function()
{
	return this.name;
};

self.setName = function(name)
{
	this.name = name;
	return this;
};

self.getDescription = function()
{
	return self.description;
};

self.setDescription = function(description)
{
	this.description = description;
	return this;
};

self.getInitialValue = function()
{
	return this.InitialValue
};

self.setInitialValue = function(initialValue)
{
	this.initialValue = initialValue;
	return this;
};

self.isNullable = function()
{
	return this.nullable;
};

self.setNullable = function(nullable)
{
	this.nullable = nullable;
	return this;
};

self.getType = function()
{
	return this.type;
};

self.setType = function(type)
{
	this.type = type;
	return this;
};

self.getProperty = function(propertyName)
{
	return this.properties[propertyName];
};

self.setProperty = function(propertyName, propertyValue)
{
	this.properties[propertyName] = propertyValue;
	return this;
};
