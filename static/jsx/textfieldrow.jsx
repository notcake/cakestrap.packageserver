var TextFieldRow = React.createClass(
	{
		render: function()
		{
			return (
				<div className="form-group" style={ { marginBottom: "2px", whiteSpace: "nowrap" } }>
					<FieldLabel text={ this.props.label } />
					<FieldText text={ this.props.text } placeholder={ this.props.placeholder } />
					<div style={ { clear: "both" } } />
				</div>
			);
		}
	}
);

TextFieldRow = StyleDecorator(TextFieldRow);
