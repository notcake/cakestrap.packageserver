var TextEntry = React.createClass(
	{
		getInitialState: function()
		{
			return { text: this.props.text }
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
				this.setState({ text: nextProps.text });
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
			this.setState({ text: event.target.value });
			
			if (this.props.onTextChanged)
			{
				this.props.onTextChanged(event.target.value);
			}
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
