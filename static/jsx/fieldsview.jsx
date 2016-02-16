var FieldsView = React.createClass(
	{
		render: function()
		{
			var fields = [];
			
			this.props.fields.forEach(
				function(field)
				{
					var text = null;
					var note = null;
					
					if (this.props.item)
					{
						var fieldValue = this.props.item[field.getName()];
						text = fieldValue;
						if (field.getProperty("formatter"))
						{
							text = field.getProperty("formatter")(this.props.item, fieldValue);
						}
						
						if (field.getProperty("noteFormatter"))
						{
							note = field.getProperty("noteFormatter")(this.props.item, fieldValue);
						}
					}
					
					fields.push(
						<TextFieldRow
							ref={ field.getName() }
							label={ field.getProperty("label") }
							text={ text }
							multiline={ field.getProperty("multiline") }
							note={ note }
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
