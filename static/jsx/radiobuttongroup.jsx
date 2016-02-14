var RadioButtonGroup = React.createClass(
	{
		getInitialState: function()
		{
			return { value: this.props.value }
		},
		
		render: function()
		{
			return (
				<span>
					{
						React.Children.map(this.props.children,
							function(child)
							{
								if (child.type != RadioButton) { return child; }
								
								return React.addons.cloneWithProps(child,
									{
										checked: this.state.value == child.props.value,
										onCheckedChange: function(checked)
										{
											if (!checked) { return; }
											
											this.setValue(child.props.value);
										}.bind(this)
									}
								);
							}.bind(this)
						)
					}
				</span>
			);
		},
		
		componentWillReceiveProps: function(nextProps)
		{
			if (this.props.value != nextProps.value)
			{
				this.setValue(nextProps.value);
			}
		},
		
		componentWillUpdate: function(nextProps, nextState)
		{
			if (this.state.value != nextState.value)
			{
				if (this.props.onValueChanged)
				{
					this.props.onValueChanged(nextState.value);
				}
			}
		},
		
		setValue: function(value)
		{
			this.setState({ value: value });
		}
	}
);
