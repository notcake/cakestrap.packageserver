function StyleDecorator(object)
{
	var methodTable = typeof(object) == "function" ? object.prototype : object;
	
	var render = methodTable.render;
	
	methodTable.render = function()
	{
		var visible = this.props.visible;
		if (visible == undefined)
		{
			visible = true;
		}
		
		var element = render.call(this);
		element.style = Object.assign(
			{},
			this.props.style || {},
			this.props.visible ? {} : { display: "none" },
			element.style
		);
		
		return element;
	};
	
	return object;
}
