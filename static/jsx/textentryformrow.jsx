var TextEntryFormRow = React.createClass(
	{
		getInitialState: function()
		{
			return {
				validationController: this.props.validationController || this.createValidationController(),
				text: this.props.text || ""
			};
		},
		
		render: function()
		{
			return (
				<div className="form-group" style={ { marginBottom: "2px", whiteSpace: "nowrap" } }>
					<FieldLabel text={ this.props.label } />
					<FieldTextEntry ref="textentry" className={ this.state.validationController.getResultState().toClassName() } placeholder={ this.props.placeholder } text={ this.props.text } multiline={ this.props.multiline } onTextChanged={ this.handleTextChanged } onEnter={ this.handleEnter } onBlur={ this.handleBlur } />
					<div style={ { display: "inline-block" } }></div>
					<ResultStatus resultState={ this.state.validationController.getResultState() } style={ { display: "inline-block", padding: "4px 8px" } } />
					<div style={ { clear: "both" } } />
				</div>
			);
		},
		
		componentWillMount: function()
		{
			this.handleValidationControllerChanged(null, this.state.validationController);
		},
		
		componentWillReceiveProps: function(nextProps)
		{
			if (this.props.text != nextProps.text)
			{
				this.setText(nextProps.text);
			}
			
			if (this.props.validationController != nextProps.validationController)
			{
				this.setState({ validationController: nextProps.validationController || this.createValidationController() });
			}
		},
		
		componentWillUpdate: function(nextProps, nextState)
		{
			this.handleValidationControllerChanged(this.state.validationController, nextState.validationController);
			
			if (this.state.text != nextState.text)
			{
				if (this.props.onTextChanged)
				{
					this.props.onTextChanged(nextState.text);
				}
			}
		},
		
		componentWillUnmount: function()
		{
			this.handleValidationControllerChanged(this.state.validationController, null);
		},
		
		focus: function ()
		{
			this.refs.textentry.focus();
		},
		
		select: function ()
		{
			this.refs.textentry.select();
		},
		
		setText: function(text)
		{
			this.setState({ text: text });
		},
		
		validate: function(text)
		{
			if (text == null)
			{
				text = this.state.text;
			}
			
			this.state.validationController.setValue(text);
		},
		
		handleTextChanged: function(text)
		{
			this.setText(text);
			this.validate(text);
		},
		
		handleEnter: function(text)
		{
			this.validate();
			
			if (this.props.onEnter)
			{
				this.props.onEnter(text);
			}
		},
		
		handleBlur: function(text)
		{
			this.validate();
			
			if (this.props.onBlur)
			{
				this.props.onBlur(text);
			}
		},
		
		handleValidationControllerChanged: function(previousValidationController, nextValidationController)
		{
			if (previousValidationController == nextValidationController) { return; }
			
			this.unhookValidationController(previousValidationController);
			this.hookValidationController(nextValidationController);
		},
		
		handleValidationStateChanged: function()
		{
			this.forceUpdate();
		},
		
		createValidationController: function(validationController)
		{
			var validationController = new ValidationController();
			validationController.setValidator(
				function(object, value, validationCallback)
				{
					if (this.props.validator)
					{
						return this.props.validator(object, value, validationCallback);
					}
					
					validationCallback(true);
				}.bind(this)
			);
			
			return validationController;
		},
		
		hookValidationController: function(validationController)
		{
			if (!validationController) { return; }
			
			validationController.validationStateChanged.addListener(this.handleValidationStateChanged);
		},
		
		unhookValidationController: function(validationController)
		{
			if (!validationController) { return; }
			
			validationController.validationStateChanged.removeListener(this.handleValidationStateChanged);
		}
	}
);

TextEntryFormRow = StyleDecorator(TextEntryFormRow);
