var FieldText = React.createClass(
	{
		render: function()
		{
			var props = Object.assign({}, this.props);
			delete props.className;
			delete props.style;
			
			return (
				<FieldContent style={ { padding: "5px 0px" } }>
					<span {...props} ref="text" style={ { whiteSpace: this.props.multiline ? "pre-line" : "normal" } }>
						{ this.props.text != null ? this.props.text : <Placeholder text={ this.props.placeholder || "None" } /> }
					</span>
					{
						this.props.note != null ? <Note text={ this.props.note } /> : null
					}
				</FieldContent>
			);
		}
	}
);

FieldText = StyleDecorator(FieldText);
