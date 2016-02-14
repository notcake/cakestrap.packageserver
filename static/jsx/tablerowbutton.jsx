var TableRowButton = React.createClass(
	{
		render: function()
		{
			return (
				<a className="block" href={ this.props.href || "#" } style={ { float: "right", padding: "8px" } }>
					<Icon icon={ this.props.icon } />
				</a>
			);
		}
	}
);

TableRowButton = StyleDecorator(TableRowButton);
