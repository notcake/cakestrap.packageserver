import json

import flask
from flask import Blueprint
from flask import g

from models import User, Package

def PackagesBlueprint(app):
	blueprint = Blueprint("packages", __name__)
	
	@blueprint.route("/packages/<int:packageId>")
	def package(packageId):
		return flask.render_template("packages/package.html", packageId = packageId)
	
	@blueprint.route("/packages/all")
	def all():
		return flask.render_template("packages/all.html")
	
	@blueprint.route("/packages/create")
	def create():
		return flask.render_template("packages/create.html")
	
	@blueprint.route("/packages/<int:packageId>.json")
	def package_json(packageId):
		package = Package.getById(g.databaseSession, packageId)
		if package is not None: package = package.toDictionary()
		return app.response_class(json.dumps(package), mimetype = "application/json")
	
	@blueprint.route("/packages/<int:packageId>.jsonp")
	def package_jsonp(packageId):
		package = Package.getById(g.databaseSession, packageId)
		if package is not None: package = package.toDictionary()
		return app.response_class("var package = " + json.dumps(package), mimetype = "application/json")
	
	@blueprint.route("/packages/all.json")
	def all_json():
		packages = Package.getAll(g.databaseSession)
		packages = [ package.toDictionary() for package in packages ]
		return app.response_class(json.dumps(packages), mimetype = "application/json")
	
	@blueprint.route("/packages/all.jsonp")
	def all_jsonp():
		packages = Package.getAll(g.databaseSession)
		packages = [ package.toDictionary() for package in packages ]
		return app.response_class("var packages = " + json.dumps(packages), mimetype = "application/json")
	
	return blueprint
