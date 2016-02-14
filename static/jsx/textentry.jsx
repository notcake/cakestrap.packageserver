var TextEntry = React.createClass(
	{
		getInitialState: function()
		{
			return { text: this.props.text || "" }
		},
		
		render: function()
		{
			if (!this.props.multiline)
			{
				return (
					<input className="form-control" type="text" placeholder={ this.props.placeholder } value={ this.state.text } onChange={ this.handleChange } onKeyUp={ this.handleKeyUp } onBlur={ this.handleBlur } />
				);
			}
			else
			{
				return (
					<textarea className="form-control" placeholder={ this.props.placeholder } value={ this.state.text } onChange={ this.handleChange } onKeyUp={ this.handleKeyUp } onBlur={ this.handleBlur } />
				);
			}
		},
		
		componentWillReceiveProps: function(nextProps)
		{
			if (this.props.text != nextProps.text)
			{
				this.setText(nextProps.text);
			}
		},
		
		componentWillUpdate: function(nextProps, nextState)
		{
			if (this.state.text != nextState.text)
			{
				if (this.props.onTextChanged)
				{
					this.props.onTextChanged(nextState.text);
				}
			}
		},
		
		focus: function()
		{
			React.findDOMNode(this).focus();
		},
		
		select: function()
		{
			React.findDOMNode(this).select();
		},
		
		setText: function(text)
		{
			this.setState({ text: text });
		},
		
		handleClick: function(event)
		{
			if (!this.props.href)
			{
				event.preventDefault();
			}
			
			if (this.props.onClick)
			{
				this.props.onClick(event);
			}
		},
		
		handleChange: function(event)
		{
			this.setText(event.target.value);
		},
		
		handleKeyUp: function(event)
		{
			if (event.keyCode == 13)
			{
				if (this.props.onEnter)
				{
					event.preventDefault();
					
					this.props.onEnter(event);
				}
			}
		},
		
		handleBlur: function(event)
		{
			if (this.props.onBlur)
			{
				this.props.onBlur(event);
			}
		}
	}
);

TextEntry = StyleDecorator(TextEntry);
