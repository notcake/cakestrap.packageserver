import json

import flask
from flask import Blueprint
from flask import g

import api
from models import User, Package, DirectoryTree

def PackagesBlueprint(app):
	blueprint = Blueprint("packages", __name__)
	
	@blueprint.route("/packages/<int:packageId>")
	def package(packageId):
		return flask.render_template("packages/package.html", packageId = packageId)
	
	@blueprint.route("/packages/")
	@blueprint.route("/packages/all")
	def all():
		return flask.render_template("packages/all.html")
	
	@blueprint.route("/packages/create", methods = ["GET"])
	def create():
		return flask.render_template("packages/create.html")
	
	@blueprint.route("/packages.json",  defaults = { "type": "json"  })
	@blueprint.route("/packages.jsonp", defaults = { "type": "jsonp" })
	@blueprint.route("/packages/all.json",  defaults = { "type": "json"  })
	@blueprint.route("/packages/all.jsonp", defaults = { "type": "jsonp" })
	@api.json()
	@api.jsonp("var packages = {}.map(Package.create);")
	@api.mapArray("toDictionary")
	def allJson(type):
		return Package.getAll(g.databaseSession)
	
	@blueprint.route("/packages/<int:packageId>.json",  defaults = { "type": "json"  })
	@blueprint.route("/packages/<int:packageId>.jsonp", defaults = { "type": "jsonp" })
	@blueprint.route("/packages/<int:packageId>/package.json",  defaults = { "type": "json"  })
	@blueprint.route("/packages/<int:packageId>/package.jsonp", defaults = { "type": "jsonp" })
	@api.json()
	@api.jsonp("var package = new Package({});")
	def packageJson(packageId, type):
		package = Package.getById(g.databaseSession, packageId)
		if package is None: return None
		return package.toDictionaryRecursive(g.currentUser == package.creatorUser)
	
	@blueprint.route("/packages/<int:packageId>/edit", methods = ["GET"])
	def packageEdit(packageId):
		return flask.render_template("packages/edit.html", packageId = packageId)
	
	@blueprint.route("/packages/create", methods = ["POST"], defaults = { "packageId": None })
	@blueprint.route("/packages/<int:packageId>/edit", methods = ["POST"])
	@api.json()
	def packageEditPost(packageId):
		json = flask.request.get_json()
		
		# Verify permissions
		if packageId is None:
			if g.currentUser is None: return api.jsonMissingActionPermissionFailure("create packages")
		else:
			if g.currentUser is None: return api.jsonMissingActionPermissionFailure("edit packages")
		
		package = Package.getById(g.databaseSession, packageId)
		
		if packageId is None:
			if not g.currentUser.canCreatePackages(): return api.jsonMissingActionPermissionFailure("create packages")
			
			package = Package()
		else:
			if package is None: return api.jsonFailure("The package does not exist or has been deleted.")
			if not g.currentUser.canEditPackage(package): return api.jsonMissingActionPermissionFailure("edit packages")
		
		# Validate Package and DirectoryTrees
		valid, validationResult = Package.validateFormFieldsDictionary(json["package"])
		if not valid: return dict(validationResult, **{ "success": False, "object": "package" })
		
		package.fromFormFieldsDictionary(g.databaseSession, json["package"])
		namedPackage = Package.getByName(g.databaseSession, package.name)
		if namedPackage is not None and namedPackage != package: return { "success": False, "object": "package", "field": "name", "message": "A package with this name already exists!" }
		
		valid, validationResult = DirectoryTree.validateFormFieldsDictionary(json["codeDirectoryTree"])
		if not valid: return dict(validationResult, **{ "success": False, "object": "package" })
		valid, validationResult = DirectoryTree.validateFormFieldsDictionary(json["resourcesDirectoryTree"])
		if not valid: return dict(validationResult, **{ "success": False, "object": "package" })
		
		# Commit Package
		if package.id is None:
			package.creatorUser = g.currentUser
			g.databaseSession.add(package)
		
		# Commit DirectoryTrees
		package.setCodeDirectoryTreeFromFormFieldsDictionary(g.databaseSession, json["codeDirectoryTree"])
		package.setResourcesDirectoryTreeFromFormFieldsDictionary(g.databaseSession, json["resourcesDirectoryTree"])
		
		g.databaseSession.commit()
		
		return { "success": True, "id": package.id }
	
	@blueprint.route("/packages/<int:packageId>/delete", methods = ["GET"])
	def packageDelete(packageId):
		return flask.render_template("packages/delete.html", packageId = packageId)
	
	@blueprint.route("/packages/<int:packageId>/delete", methods = ["POST"])
	@api.json()
	def packageDeletePost(packageId):
		if g.currentUser is None: return api.jsonMissingActionPermissionFailure("delete packages")
		
		package = Package.getById(g.databaseSession, packageId)
		
		if package is None: return api.jsonFailure("The package does not exist or has been deleted.")
		if not g.currentUser.canDeletePackage(package): return api.jsonMissingActionPermissionFailure("delete packages")
		
		package.remove(g.databaseSession)
		g.databaseSession.commit()
		
		return { "success": True }
	
	@blueprint.route("/packages/named.json")
	@api.json()
	@api.map("toDictionary")
	def namedJson():
		return Package.getByName(g.databaseSession, flask.request.args.get("name", ""))
	
	return blueprint
