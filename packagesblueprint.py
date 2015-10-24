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
	
	@blueprint.route("/packages/all")
	def all():
		return flask.render_template("packages/all.html")
	
	@blueprint.route("/packages/create", methods = ["GET"])
	def create():
		return flask.render_template("packages/create.html")
	
	@blueprint.route("/packages/create", methods = ["POST"])
	@api.json()
	def createPost():
		if g.currentUser is None or not g.currentUser.canCreatePackages():
			return { "success": False, "message": "You do not have permission to create packages." }
		
		# Prepare data
		package = Package()
		package.creatorUser = g.currentUser
		package.name        = flask.request.form.get("name", "")
		package.displayName = flask.request.form.get("displayName", "")
		package.description = flask.request.form.get("description", "")
		if package.name        == "": return { "success": False, "message": "You must provide a package name!", "field": "name"        }
		if package.displayName == "": package.displayName = package.name
		if package.description == "": return { "success": False, "message": "You must provide a description!",  "field": "description" }
		if Package.getByName(g.databaseSession, package.name) is not None: return { "success": False, "message": "A package with this name already exists!", "field": "name" }
		
		repositoryUrl = flask.request.form.get("gitRepositoryUrl", "")
		if repositoryUrl == "": repositoryUrl = None
		
		# Prepare data
		packageGitRepository = PackageGitRepository()
		packageGitRepository.package       = package
		packageGitRepository.branch        = flask.request.form.get("gitBranch",    "")
		packageGitRepository.revision      = flask.request.form.get("gitRevision",  "")
		packageGitRepository.directory     = flask.request.form.get("gitDirectory", "")
		if packageGitRepository.branch   == "": packageGitRepository.branch   = None
		if packageGitRepository.revision == "": packageGitRepository.revision = None
		
		if repositoryUrl is None and \
		   (packageGitRepository.branch is not None or \
		    packageGitRepository.revision is not None or \
		    packageGitRepository.directory != ""):
			return { "success": False, "message": "You must provide a repository URL!",  "field": "gitRepositoryUrl" }
		
		if packageGitRepository.branch is None: packageGitRepository.branch = "master"
		
		# Begin committing changes
		g.databaseSession.add(package)
		
		if repositoryUrl is not None:
			GitRepository.addRef(g.databaseSession, repositoryUrl, packageGitRepository)
			g.databaseSession.add(packageGitRepository)
		
		g.databaseSession.commit()
		
		return { "success": True, "id": package.id }
	
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
