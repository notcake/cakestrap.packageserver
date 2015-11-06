var FieldsEditor = React.createClass(
	{
		render: function()
		{
			var fields = [];
			
			this.props.fields.forEach(
				function(field, i)
				{
					var validator     = null;
					var onTextChanged = null;
					var onEnter       = null;
					
					if (field.getProperty("validator"))
					{
						validator = function(_, value, validationCallback)
						{
							return field.getProperty("validator").call(this, this.props.item, value, validationCallback);
						}.bind(this);
					}
					
					onTextChanged = function(value)
					{
						if (field.getProperty("onTextChanged"))
						{
							field.getProperty("onTextChanged").call(this, this.props.item, value);
						}
						
						this.props.item[field.getName()] = value;
					}.bind(this);
					
					onEnter = function(event)
					{
						if (this.props.fields[i + 1])
						{
							this.refs[this.props.fields[i + 1].getName()].select();
						}
						else if (this.props.onEnter)
						{
							this.props.onEnter(event);
						}
						
						if (field.getProperty("onEnter"))
						{
							field.getProperty("onEnter").call(this, event);
						}
					}.bind(this);
					
					fields.push(
						<TextEntryFormRow
							ref={ field.getName() }
							label={ field.getProperty("label") }
							text={ this.props.item && this.props.item[field.getName()] }
							placeholder={ field.getProperty("placeholder") }
							multiline={ field.getProperty("multiline") }
							validator={ validator }
							onTextChanged={ onTextChanged }
							onEnter={ onEnter }
						/>
					);
				}.bind(this)
			);
			
			return (
				<div>
					{ fields }
				</div>
			);
		},
		
		focus: function(fieldName)
		{
			if (fieldName == null) { fieldName = this.getFirstFieldName(); }
			if (!this.refs[fieldName]) { return; }
			this.refs[fieldName].focus();
		},
		
		select: function(fieldName)
		{
			if (fieldName == null) { fieldName = this.getFirstFieldName(); }
			if (!this.refs[fieldName]) { return; }
			this.refs[fieldName].select();
		},
		
		validate: function(fieldName, fieldValue)
		{
			if (fieldName != null)
			{
				if (!this.refs[fieldName]) { return; }
				this.refs[fieldName].validate(fieldValue);
				return;
			}
			
			for (var i in this.props.fields)
			{
				this.refs[this.props.fields[i].getName()].validate();
			}
		},
		
		getFirstFieldName: function()
		{
			if (this.props.fields.length == 0) { return null; }
			
			return this.props.fields[0].getName();
		}
	}
);

function FieldsEditorFactory(fields)
{
	return React.createClass(
		{
			render: function()
			{
				return <FieldsEditor { ...this.props } ref="fields" fields={ fields } />;
			},
			
			focus:    function(fieldName) { this.refs.fields.focus(fieldName);    },
			select:   function(fieldName) { this.refs.fields.select(fieldName);   },
			validate: function(fieldName) { this.refs.fields.validate(fieldName); },
		}
	);
}
