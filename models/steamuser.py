from sqlalchemy import select, func
from sqlalchemy import Column, PrimaryKeyConstraint, ForeignKey, UniqueConstraint
from sqlalchemy import Boolean, Integer, BigInteger, Text
from sqlalchemy import Enum
from sqlalchemy.orm import relationship, column_property

from base import Base

class SteamUser(Base):
	__tablename__           = "steam_users"
	
	steamId64               = Column("steamid64",                  BigInteger, nullable = False)
	displayName             = Column("display_name",               Text,       nullable = False)
	smallProfilePictureUrl  = Column("small_profile_picture_url",  Text,       nullable = False)
	mediumProfilePictureUrl = Column("medium_profile_picture_url", Text,       nullable = False)
	largeProfilePictureUrl  = Column("large_profile_picture_url",  Text,       nullable = False)
	
	PrimaryKeyConstraint(steamId64)
	
	@classmethod
	def getBySteamId64(cls, databaseSession, steamId64):
		steamUser = databaseSession.query(cls).filter(cls.steamId64 == steamId64).first()
		return steamUser
	
	@classmethod
	def registerSteamUser(cls, databaseSession, steamUserInformation):
		steamUser = cls.getBySteamId64(databaseSession, steamUserInformation.steamId64)
		if steamUser is None:
			steamUser = cls()
			steamUser.steamId64 = steamUserInformation.steamId64
			databaseSession.add(steamUser)
		
		steamUser.displayName             = steamUserInformation.displayName
		steamUser.smallProfilePictureUrl  = steamUserInformation.smallProfilePictureUrl
		steamUser.mediumProfilePictureUrl = steamUserInformation.mediumProfilePictureUrl
		steamUser.largeProfilePictureUrl  = steamUserInformation.largeProfilePictureUrl
		databaseSession.commit()
		
		return steamUser
