NonNullableValidator = function(message, compact)
{
	if (compact)
	{
		message = "You must provide " + message + "!";
	}
	
	return function(object, value, validationCallback)
	{
		if (value == "")
		{
			validationCallback(false, message);
			return;
		}
		
		validationCallback(true);
	};
};
