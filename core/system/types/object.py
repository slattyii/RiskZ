from munch import DefaultMunch as _DefaultMunch

class Object(_DefaultMunch):
	def __repr__(self):
		return str(self.toDict())
	
	@staticmethod
	def valueOf(obj = {}):
		return Object.fromDict(obj, Object.fromDict({}))