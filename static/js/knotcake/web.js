var Knotcake = Knotcake || {}
Knotcake.Web = Knotcake.Web || {}

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
}

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
}
