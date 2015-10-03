from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, BigInteger, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
	__tablename__ = "users"
	
	id                      = Column("id", BigInteger, primary_key = True)
	steamId64               = Column("steamid64", BigInteger, unique = True)
	displayName             = Column("display_name", Text)
	smallProfilePictureUrl  = Column("small_profile_picture_url", Text)
	mediumProfilePictureUrl = Column("medium_profile_picture_url", Text)
	largeProfilePictureUrl  = Column("large_profile_picture_url", Text)
	
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
			databaseSession.add(user)
		
		user.displayName             = steamUser.displayName
		user.smallProfilePictureUrl  = steamUser.smallProfilePictureUrl
		user.mediumProfilePictureUrl = steamUser.mediumProfilePictureUrl
		user.largeProfilePictureUrl  = steamUser.largeProfilePictureUrl
		databaseSession.commit()
		
		return user
