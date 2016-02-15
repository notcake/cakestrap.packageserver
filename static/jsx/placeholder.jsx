var Placeholder = React.createClass(
	{
		render: function()
		{
			return (
				<span style={ { color: "gray", fontStyle: "italic" } }>
					{ this.props.text }
					{ this.props.children }
				</span>
			);
		}
	}
);

Placeholder = StyleDecorator(Placeholder);
