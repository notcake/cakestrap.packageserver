var ColoredBox = React.createClass(
	{
		render: function()
		{
			return (
				<div { ...this.props } className="colored-box" style={ { backgroundColor: this.props.color } }>
					{ this.props.children }
				</div>
			);
		}
	}
);

ColoredBox = StyleDecorator(ColoredBox);
