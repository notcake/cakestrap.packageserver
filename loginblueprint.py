import flask
from flask import Blueprint

import knotcake.steam

blueprint = Blueprint("login", __name__)

steamOpenId = knotcake.steam.OpenId()
steamOpenId.localUrl = "http://packages.knotcake.net/login"

@blueprint.route("/login")
def login():
	return flask.redirect(steamOpenId.generateLoginUrl())

@blueprint.route("/logout")
def logout():
	return "HI2"
