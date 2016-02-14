var ContentBox = React.createClass(
	{
		render: function()
		{
			return (
				<ColoredBox { ...this.props } style={ { overflow: "auto", width: "100%", margin: "8px auto", padding: "16px" } }>
					{ this.props.children }
				</ColoredBox>
			);
		}
	}
);

ContentBox = StyleDecorator(ContentBox);
