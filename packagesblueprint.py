import json

import flask
from flask import Blueprint
from flask import g

import api
from models import User, Package, PackageGitRepository, GitRepository

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
	
	@blueprint.route("/packages/<int:packageId>.json",  defaults = { "type": "json"  })
	@blueprint.route("/packages/<int:packageId>.jsonp", defaults = { "type": "jsonp" })
	@blueprint.route("/packages/<int:packageId>/package.json",  defaults = { "type": "json"  })
	@blueprint.route("/packages/<int:packageId>/package.jsonp", defaults = { "type": "jsonp" })
	@api.json()
	@api.jsonp("var package = new Package({});")
	@api.map("toDictionary")
	def packageJson(packageId, type):
		return Package.getById(g.databaseSession, packageId)
	
	@blueprint.route("/packages/<int:packageId>/gitrepository.json",  defaults = { "type": "json"  })
	@blueprint.route("/packages/<int:packageId>/gitrepository.jsonp", defaults = { "type": "jsonp" })
	@api.json()
	@api.jsonp("var packageGitRepository = new PackageGitRepository({});")
	@api.map("toDictionary")
	def packageGitRepositoryJson(packageId, type):
		return PackageGitRepository.getByPackage(g.databaseSession, packageId)
	
	@blueprint.route("/packages/<int:packageId>/edit", methods = ["GET"])
	def packageEdit(packageId):
		return flask.render_template("packages/edit.html", packageId = packageId)
	
	@blueprint.route("/packages/create", methods = ["POST"], defaults = { "packageId": None })
	@blueprint.route("/packages/<int:packageId>/edit", methods = ["POST"])
	@api.json()
	def packageEditPost(packageId):
		id = flask.request.form.get("id")
		if id == "": id = None
		
		# Verify permissions
		if id is None:
			if g.currentUser is None: return api.jsonMissingActionPermissionFailure("create packages")
		else:
			if g.currentUser is None: return api.jsonMissingActionPermissionFailure("edit packages")
		
		destinationPackage = Package.getById(g.databaseSession, id)
		
		if id is None:
			if not g.currentUser.canCreatePackages(): return api.jsonMissingActionPermissionFailure("create packages")
			
			destinationPackage = Package()
		else:
			if destinationPackage is None: return api.jsonFailure("The package does not exist or has been deleted.")
			if not g.currentUser.canEditPackage(destinationPackage): return api.jsonMissingActionPermissionFailure("edit packages")
		
		destinationPackageGitRepository = PackageGitRepository.getByPackage(g.databaseSession, destinationPackage)
		
		# Read Package
		sourcePackage = Package()
		sourcePackage.name        = flask.request.form.get("name", "")
		sourcePackage.displayName = flask.request.form.get("displayName", "")
		sourcePackage.description = flask.request.form.get("description", "")
		
		# Read PackageGitRepository
		sourcePackageGitRepository = PackageGitRepository()
		sourcePackageGitRepository.package       = destinationPackage
		sourcePackageGitRepository.branch        = flask.request.form.get("gitBranch",    "")
		sourcePackageGitRepository.revision      = flask.request.form.get("gitRevision",  "")
		sourcePackageGitRepository.directory     = flask.request.form.get("gitDirectory", "")
		
		# Validate Package
		if sourcePackage.name        == "": return { "success": False, "message": "You must provide a package name!", "field": "name"        }
		if sourcePackage.displayName == "": sourcePackage.displayName = sourcePackage.name
		if sourcePackage.description == "": return { "success": False, "message": "You must provide a description!",  "field": "description" }
		
		namedPackage = Package.getByName(g.databaseSession, sourcePackage.name)
		if namedPackage is not None and namedPackage != destinationPackage: return { "success": False, "message": "A package with this name already exists!", "field": "name" }
		
		# Validate PackageGitRepository
		if sourcePackageGitRepository.branch   == "": sourcePackageGitRepository.branch   = None
		if sourcePackageGitRepository.revision == "": sourcePackageGitRepository.revision = None
		
		repositoryUrl = flask.request.form.get("gitRepositoryUrl", "")
		if repositoryUrl == "": repositoryUrl = None
		
		previousRepositoryUrl = None
		if destinationPackageGitRepository is not None:
			previousRepositoryUrl = destinationPackageGitRepository.gitRepository.url
		
		if repositoryUrl is None and \
		   (sourcePackageGitRepository.branch is not None or \
		    sourcePackageGitRepository.revision is not None or \
		    sourcePackageGitRepository.directory != ""):
			return { "success": False, "message": "You must provide a repository URL!",  "field": "url" }
		
		if sourcePackageGitRepository.branch is None: sourcePackageGitRepository.branch = "master"
		
		# Commit Package
		if id is None: destinationPackage.creatorUser = g.currentUser
		destinationPackage.name        = sourcePackage.name
		destinationPackage.displayName = sourcePackage.displayName
		destinationPackage.description = sourcePackage.description
		
		if destinationPackage.id is None:
			g.databaseSession.add(destinationPackage)
		
		# Commit PackageGitRepository
		if previousRepositoryUrl != repositoryUrl:
			if destinationPackageGitRepository is not None:
				destinationPackageGitRepository.remove(g.databaseSession)
				destinationPackageGitRepository = None
			
			if destinationPackageGitRepository is None:
				destinationPackageGitRepository = PackageGitRepository()
				destinationPackageGitRepository.package   = sourcePackageGitRepository.package
			
			if repositoryUrl is not None:
				destinationPackageGitRepository.branch    = sourcePackageGitRepository.branch
				destinationPackageGitRepository.revision  = sourcePackageGitRepository.revision
				destinationPackageGitRepository.directory = sourcePackageGitRepository.directory
				
				GitRepository.addRef(g.databaseSession, repositoryUrl, destinationPackageGitRepository)
				g.databaseSession.add(destinationPackageGitRepository)
		elif repositoryUrl is not None:
			destinationPackageGitRepository.branch    = sourcePackageGitRepository.branch
			destinationPackageGitRepository.revision  = sourcePackageGitRepository.revision
			destinationPackageGitRepository.directory = sourcePackageGitRepository.directory
		
		g.databaseSession.commit()
		
		return { "success": True, "id": destinationPackage.id }
	
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
	
	@blueprint.route("/packages.json",  defaults = { "type": "json"  })
	@blueprint.route("/packages.jsonp", defaults = { "type": "jsonp" })
	@blueprint.route("/packages/all.json",  defaults = { "type": "json"  })
	@blueprint.route("/packages/all.jsonp", defaults = { "type": "jsonp" })
	@api.json()
	@api.jsonp("var packages = {}.map(Package.create);")
	@api.mapArray("toDictionary")
	def allJson(type):
		return Package.getAll(g.databaseSession)
	
	return blueprint
