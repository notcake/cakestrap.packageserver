import knotcake.oop

class User(knotcake.oop.Object):
	def __init__(self):
		self.steamId64 = None
		self.displayName = None
		self.profileUrl = None
		
		self.smallProfilePictureUrl = None
		self.mediumProfilePictureUrl = None
		self.largeProfilePictureUrl = None
	
	@property
	def profilePictureUrl(self):
		return self.largeProfilePictureUrl
	
	def toUserInformation(self):
		return {
			"steamid": unicode(self.steamId64),
			"personaname": self.displayName,
			"profileurl": self.profileUrl,
			
			"avatar": self.smallProfilePictureUrl,
			"avatarmedium": self.mediumProfilePictureUrl,
			"avatarlarge": self.largeProfilePictureUrl
		}
	
	def __repr__(self):
		return "User.fromUserInformation(" + repr(self.toUserInformation()) + ")"
	
	@staticmethod
	def fromUserInformation(userInformation):
		user = User()
		
		user.steamId64 = int(userInformation["steamid"])
		user.displayName = userInformation["personaname"]
		user.profileUrl = userInformation["profileurl"]
		
		user.smallProfilePictureUrl = userInformation["avatar"];
		user.mediumProfilePictureUrl = userInformation["avatarmedium"];
		user.largeProfilePictureUrl = userInformation["avatarfull"];
		
		return user
