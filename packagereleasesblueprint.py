import json

import flask
from flask import Blueprint
from flask import g

import api
from models import User, Package, PackageRelease

def PackageReleasesBlueprint(app):
	blueprint = Blueprint("packagereleases", __name__)
	
	@blueprint.route("/packages/<int:packageId>/releases.json",  defaults = { "type": "json"  })
	@blueprint.route("/packages/<int:packageId>/releases.jsonp", defaults = { "type": "jsonp" })
	@blueprint.route("/packages/<int:packageId>/releases/all.json",  defaults = { "type": "json"  })
	@blueprint.route("/packages/<int:packageId>/releases/all.jsonp", defaults = { "type": "jsonp" })
	@api.json()
	@api.jsonp("var packageReleases = {}.map(PackageRelease.create);")
	@api.mapArray("toDictionary")
	def packageReleasesJson(packageId, type):
		package = Package.getById(g.databaseSession, packageId)
		if package is None: return []
		
		return package.releases
	
	@blueprint.route("/packages/<int:packageId>/releases/<int:packageReleaseId>.json",  defaults = { "type": "json"  })
	@blueprint.route("/packages/<int:packageId>/releases/<int:packageReleaseId>.jsonp", defaults = { "type": "jsonp" })
	@blueprint.route("/packages/<int:packageId>/releases/<int:packageReleaseId>/release.json",  defaults = { "type": "json"  })
	@blueprint.route("/packages/<int:packageId>/releases/<int:packageReleaseId>/release.jsonp", defaults = { "type": "jsonp" })
	@api.json()
	@api.jsonp("var packageRelease = new PackageRelease({});")
	def packageReleaseJson(packageId, packageReleaseId, type):
		packageRelease = PackageRelease.getById(g.databaseSession, packageReleaseId)
		if packageRelease is None: return None
		
		return packageRelease.toDictionaryRecursive(g.currentUser == packageRelease.package.creatorUser)
	
	@blueprint.route("/packages/<int:packageId>/releases/create", methods = ["POST"])
	@api.json()
	def packageReleaseCreate(packageId):
		if g.currentUser is None: return api.jsonMissingActionPermissionFailure("create package releases")
		
		package = Package.getById(g.databaseSession, packageId)
		
		if package is None: return api.jsonFailure("The package does not exist or has been deleted.")
		if not g.currentUser.canEditPackage(package): return api.jsonMissingActionPermissionFailure("create package releases")
		
		package.createRelease(g.databaseSession, flask.g.time)
		g.databaseSession.commit()
		
		return { "success": True }
	
	@blueprint.route("/packages/<int:packageId>/releases/<int:packageReleaseId>", methods = ["GET"])
	def packageRelease(packageId, packageReleaseId):
		return flask.render_template("packages/releases/release.html", packageId = packageId, packageReleaseId = packageReleaseId)
	
	@blueprint.route("/packages/<int:packageId>/releases/<int:packageReleaseId>/download", methods = ["GET"])
	def packageReleaseDownload(packageId, packageReleaseId):
		packageRelease = PackageRelease.getById(g.databaseSession, packageReleaseId)
		if packageRelease is None: flask.abort(404)
		
		response = flask.send_file(packageRelease.generatePackage(), as_attachment = True, attachment_filename = packageRelease.getFullFileName(), conditional = True)
		return response
	
	@blueprint.route("/packages/<int:packageId>/releases/<int:packageReleaseId>/delete", methods = ["GET"])
	def packageReleaseDelete(packageId, packageReleaseId):
		returnPage = flask.request.args.get("returnPage", "")
		if returnPage not in ("package", "packageRelease"): returnPage = "packageRelease"
		return flask.render_template("packages/releases/delete.html", packageId = packageId, packageReleaseId = packageReleaseId, returnPage = returnPage)
	
	@blueprint.route("/packages/<int:packageId>/releases/<int:packageReleaseId>/delete", methods = ["POST"])
	@api.json()
	def packageReleaseDeletePost(packageId, packageReleaseId):
		if g.currentUser is None: return api.jsonMissingActionPermissionFailure("delete package releases")
		
		packageRelease = PackageRelease.getById(g.databaseSession, packageReleaseId)
		package        = packageRelease.package
		
		if packageRelease is None: return api.jsonFailure("The package release does not exist or has been deleted.")
		if not g.currentUser.canEditPackage(package): return api.jsonMissingActionPermissionFailure("delete package releases")
		
		packageRelease.remove(g.databaseSession)
		g.databaseSession.commit()
		
		return { "success": True }
	
	return blueprint
