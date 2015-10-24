var self = {};
var ValidationController = Knotcake.OOP.Class(self)

self.ctor = function(resultState)
{
	this.resultState = resultState || new ResultState();
	
	this.validatedValue = null;
	this.value = null;
	
	this.valueChangeSink = this.setValue.bind(this);
	this.validator = function(value, validationCallback)
	{
		validationCallback(true);
	};
	
	this.validationStateChanged = new Knotcake.OOP.Event();
};

self.getResultState = function()
{
	return this.resultState;
};

self.getValueChangeSink   = function () { return this.valueChangeSink; };
self.getCheckedChangeSink = function () { return this.valueChangeSink; };
self.getTextChangeSink    = function () { return this.valueChangeSink; };

self.setValidator = function(validator)
{
	this.validator = validator;
	return this;
};

self.setValidationResult = function(valid, message)
{
	if (valid == true) { this.resultState.success(message); }
	else if (valid == false) { this.resultState.failure(message); }
	else { this.resultState.none(message); }
	
	this.validationStateChanged.dispatch(this.resultState.getState(), this.resultState.getMessage());
	
	return this;
};

self.setValue = function(value)
{
	if (this.value == value) { return this; }
	
	this.value = value;
	
	this.validate(value);
	
	return this;
};

self.validate = function(value)
{
	if (value == this.validatedValue) { return; }
	if (this.resultState.isPending()) { return; }
	
	this.resultState.pending();
	var validationResultReceived = false;
	var validationResult = this.validator(
		value,
		function(valid, message)
		{
			this.setValidationResult(valid, message);
			this.validatedValue = value;
			
			validationResultReceived = true;
			
			if (this.value != this.validatedValue)
			{
				this.validate(this.value);
			}
		}.bind(this)
	);
	
	if (!validationResultReceived)
	{
		if (validationResult == true) { this.setValidationResult(true); }
		else if (validationResult == false) { this.setValidationResult(false); }
		else if (validationResult instanceof Array)
		{
			this.setValidationResult(validationResult[0], validationResult[1]);
		}
	}
};
