var FieldText = React.createClass(
	{
		render: function()
		{
			var props = Object.assign({}, this.props);
			delete props.className;
			delete props.style;
			
			return (
				<FieldContent style={ { padding: "5px 0px" } }>
					<span {...props} ref="text" style={ this.props.text != null ? {} : { color: "gray", fontStyle: "italic" } }>
						{ this.props.text != null ? this.props.text : (this.props.placeholder || "None") }
					</span>
				</FieldContent>
			);
		}
	}
);

FieldText = StyleDecorator(FieldText);
