var FieldLabel = React.createClass(
	{
		render: function()
		{
			return (
				<span className={ this.props.className || "col-md-3" } style={ { padding: "5px 0px" } }>
					<b>{ this.props.text }</b>
				</span>
			);
		}
	}
);

FieldLabel = StyleDecorator(FieldLabel);
