from sqlalchemy.ext.declarative import declarative_base

class Base(object):
	@classmethod
	def getAll(cls, databaseSession):
		results = databaseSession.query(cls).order_by(cls.id.desc()).all()
		return results
	
	@classmethod
	def getById(cls, databaseSession, id):
		if id is None: return None
		
		result = databaseSession.query(cls).filter(cls.id == id).first()
		return result

Base = declarative_base(cls = Base)
