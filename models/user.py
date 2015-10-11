import flask

from sqlalchemy import select, func
from sqlalchemy import Column, PrimaryKeyConstraint, ForeignKey, UniqueConstraint
from sqlalchemy import Boolean, Integer, BigInteger, Text
from sqlalchemy import Enum
from sqlalchemy.orm import relationship, column_property

from base import Base
from steamuser import SteamUser

class User(Base):
	__tablename__           = "users"
	
	id                      = Column("id",                         BigInteger, nullable = False)
	steamId64               = Column("steamid64",                  BigInteger, ForeignKey("steam_users.steamid64"), nullable = False)
	displayName             = Column("display_name",               Text,       nullable = False)
	smallProfilePictureUrl  = Column("small_profile_picture_url",  Text,       nullable = False)
	mediumProfilePictureUrl = Column("medium_profile_picture_url", Text,       nullable = False)
	largeProfilePictureUrl  = Column("large_profile_picture_url",  Text,       nullable = False)
	rank                    = Column("rank",                       Enum("user", "moderator", "administrator", "overlord"), nullable = False)
	creationTimestamp       = Column("creation_timestamp",         BigInteger, nullable = False)
	lastLoginTimestamp      = Column("last_login_timestamp",       BigInteger, nullable = True)
	lastActivityTimestamp   = Column("last_activity_timestamp",    BigInteger, nullable = True)
	
	steamUser               = relationship("SteamUser", uselist = False)
	packages                = relationship("Package",   uselist = True)
	
	PrimaryKeyConstraint(id)
	
	def __init__(self):
		self.rank = "user"
	
	def toDictionary(self, out = None):
		if out is None: out = {}
		
		out["id"]                      = str(self.id)
		out["steamId64"]               = str(self.steamId64)
		out["displayName"]             = self.displayName
		out["smallProfilePictureUrl"]  = self.smallProfilePictureUrl
		out["mediumProfilePictureUrl"] = self.mediumProfilePictureUrl
		out["largeProfilePictureUrl"]  = self.largeProfilePictureUrl
		out["rank"]                    = self.rank
		out["creationTimestamp"]       = self.creationTimestamp
		out["lastLoginTimestamp"]      = self.lastLoginTimestamp
		out["lastActivityTimestamp"]   = self.lastActivityTimestamp
		
		return out
	
	@classmethod
	def getAll(cls, databaseSession):
		users = databaseSession.query(User).order_by(User.creationTimestamp.desc()).all()
		return users
	
	@classmethod
	def getById(cls, databaseSession, id):
		user = databaseSession.query(User).filter(User.id == id).first()
		return user
	
	@classmethod
	def getBySteamId64(cls, databaseSession, steamId64):
		user = databaseSession.query(User).filter(User.steamId64 == steamId64).first()
		return user
	
	@classmethod
	def registerSteamUser(cls, databaseSession, steamUser):
		user = User.getBySteamId64(databaseSession, steamUser.steamId64)
		if user is None:
			user = User()
			user.steamId64 = steamUser.steamId64
			user.creationTimestamp = flask.g.time
			databaseSession.add(user)
		
		user.displayName             = steamUser.displayName
		user.smallProfilePictureUrl  = steamUser.smallProfilePictureUrl
		user.mediumProfilePictureUrl = steamUser.mediumProfilePictureUrl
		user.largeProfilePictureUrl  = steamUser.largeProfilePictureUrl
		databaseSession.commit()
		
		return user
