var Knotcake = Knotcake || {};
Knotcake.Web = Knotcake.Web || {};

Knotcake.Web.Get = function(url, parameters, successCallback, failureCallback)
{
	$.ajax(
		{
			url:     url,
			type:    "GET",
			data:    parameters,
			success: successCallback
		}
	).fail(failureCallback);
};

Knotcake.Web.GetBinary = function(url, parameters, successCallback, failureCallback)
{
	var xhr = new XMLHttpRequest();
	xhr.open("GET", url, true);
	xhr.responseType = "blob";
	
	xhr.onload = function(event)
	{
		successCallback(xhr.response, "success", xhr);
	};
	
	xhr.send();
};

Knotcake.Web.Post = function(url, json, successCallback, failureCallback)
{
	$.ajax(
		{
			url:         url,
			type:        "POST",
			data:        JSON.stringify(json),
			contentType: "application/json; charset=utf-8",
			success:     successCallback
		}
	).fail(failureCallback);
};
