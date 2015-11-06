var FieldsView = React.createClass(
	{
		render: function()
		{
			var fields = [];
			
			this.props.fields.forEach(
				function(field)
				{
					fields.push(
						<TextFieldRow
							ref={ field.getName() }
							label={ field.getProperty("label") }
							text={ this.props.item && this.props.item[field.getName()] }
						/>
					);
				}.bind(this)
			);
			
			return (
				<div>
					{ fields }
				</div>
			);
		}
	}
);

function FieldsViewFactory(fields)
{
	return React.createClass(
		{
			render: function()
			{
				return <FieldsView { ...this.props } fields={ fields } />;
			}
		}
	);
}
