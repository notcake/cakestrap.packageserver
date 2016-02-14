var FieldText = React.createClass(
	{
		render: function()
		{
			var props = Object.assign({}, this.props);
			delete props.className;
			delete props.style;
			
			return (
				<FieldContent style={ { padding: "5px 0px" } }>
					<span {...props} ref="text">
						{ this.props.text != null ? this.props.text : <Note text={ this.props.placeholder || "None" } /> }
					</span>
				</FieldContent>
			);
		}
	}
);

FieldText = StyleDecorator(FieldText);
