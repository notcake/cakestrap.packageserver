var ButtonGroup = React.createClass(
	{
		render: function()
		{
			return (
				<div className="btn-group">
					{ this.props.children }
				</div>
			);
		}
	}
);

ButtonGroup = StyleDecorator(ButtonGroup);
