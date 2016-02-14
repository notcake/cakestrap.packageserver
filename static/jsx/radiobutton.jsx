var RadioButton = React.createClass(
	{
		getInitialState: function()
		{
			return { checked: this.props.checked || false }
		},
		
		render: function()
		{
			return (
				<label style={ { verticalAlign: "middle", marginRight: "32px", cursor: "default", fontWeight: "normal" } }>
					<input ref="radio" style={ { marginRight: "4px" } } type="radio" checked={ this.state.checked } onChange={ this.handleChange } text={ this.props.text }/>
					{ this.props.text }
				</label>
			);
		},
		
		componentWillReceiveProps: function(nextProps)
		{
			if (this.props.checked != nextProps.checked)
			{
				this.setChecked(nextProps.checked);
			}
		},
		
		componentWillUpdate: function(nextProps, nextState)
		{
			if (this.state.checked != nextState.checked)
			{
				if (this.props.onCheckedChange)
				{
					this.props.onCheckedChange(nextState.checked);
				}
			}
		},
		
		setChecked: function(checked)
		{
			this.setState({ checked: checked });
		},
		
		handleChange: function(event)
		{
			this.setChecked(event.target.checked);
		},
	}
);

RadioButton = StyleDecorator(RadioButton);
