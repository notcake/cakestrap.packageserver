var FieldTextEntry = React.createClass(
	{
		render: function()
		{
			var props = Object.assign({}, this.props);
			delete props.className;
			delete props.style;
			
			return (
				<FieldContent>
					<TextEntry {...props} ref="textentry" style={ { width: "100%" } } />
				</FieldContent>
			);
		},
	
		focus: function ()
		{
			this.refs.textentry.focus();
		},
		
		select: function ()
		{
			this.refs.textentry.select();
		}
	}
);

FieldTextEntry = StyleDecorator(FieldTextEntry);
