import functools
import operator
import types

import flask

def toMapFunction(mapFunction):
	if type(mapFunction) in types.StringTypes:
		mapFunction = operator.methodcaller(mapFunction)
	
	return mapFunction

def map(mapFunction):
	mapFunction = toMapFunction(mapFunction)
	
	def map(f):
		@functools.wraps(f)
		def map(*args, **kwargs):
			object = f(*args, **kwargs)
			if object is None: return None
			return mapFunction(object)
		
		return map
	
	return map

def mapArray(mapFunction):
	mapFunction = toMapFunction(mapFunction)
	
	def mapArray(f):
		@functools.wraps(f)
		def mapArray(*args, **kwargs):
			objects = f(*args, **kwargs)
			return [ mapFunction(x) for x in objects ]
		
		return mapArray
	
	return mapArray

def json():
	def json(f):
		@functools.wraps(f)
		def json(*args, **kwargs):
			import json
			
			object = f(*args, **kwargs)
			
			if isinstance(object, flask.Response): return object
			if "type" in kwargs and kwargs["type"] != "json": return object
			
			indent = None
			if int(flask.request.args.get("pretty", 0)): indent = 4
			object = json.dumps(object, indent = indent)
			object = flask.Response(object, mimetype = "application/json")
			return object
		
		return json
	
	return json

def jsonp(expression):
	import json
	
	def jsonp(f):
		@functools.wraps(f)
		def jsonp(*args, **kwargs):
			object = f(*args, **kwargs)
			
			if isinstance(object, flask.Response): return object
			if "type" in kwargs and kwargs["type"] != "jsonp": return object
			
			indent = None
			if int(flask.request.args.get("pretty", 0)): indent = 4
			object = json.dumps(object, indent = indent)
			object = expression.format(object)
			object = flask.Response(object, mimetype = "application/javascript")
			return object
		
		return jsonp
	
	return jsonp

def jsonFailure(message):
	return { "success": False, "message": message }

def jsonMissingActionPermissionFailure(actionDisplayName):
	return jsonFailure("You do not have permission to " + actionDisplayName + ".")
