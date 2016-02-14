var Knotcake = Knotcake || {};
Knotcake.OOP = Knotcake.OOP || {};

Knotcake.OOP.Class = function(methodTable, baseClass)
{
	var instanceConstructor = function()
	{
		if (this.ctor)
		{
			this.ctor.apply(this, arguments);
		}
		
		return this;
	};
	
	instanceConstructor.prototype = methodTable;
	instanceConstructor.create = function()
	{
		return new (instanceConstructor.bind.bind(instanceConstructor, instanceConstructor).apply(instanceConstructor, arguments));
	};
	
	return instanceConstructor;
};
