var Note = React.createClass(
	{
		render: function()
		{
			return (
				<span style={ { color: "gray", fontSize: "90%", marginLeft: "4px" } }>
					{ "(" }
					{ this.props.text }
					{ this.props.children }
					{ ")" }
				</span>
			);
		}
	}
);

Note = StyleDecorator(Note);
