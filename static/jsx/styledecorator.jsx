function StyleDecorator(object)
{
	var methodTable = typeof(object) == "function" ? object.prototype : object;
	
	var render = methodTable.render;
	
	methodTable.render = function()
	{
		var visible = this.props.visible;
		if (visible === undefined)
		{
			visible = true;
		}
		
		var element = render.call(this);
		if (!element) { return element; }
		
		element.props.style = Object.assign(
			{},
			this.props.style || {},
			visible ? {} : { display: "none" },
			element.props.style
		);
		
		if (this.props.className)
		{
			element.props.className += " " + this.props.className;
		}
		
		return element;
	};
	
	return object;
}
