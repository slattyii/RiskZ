import json
from core.system.types.object import Object

class Rson:
	@staticmethod
	def file(path):
		try:
			with open(path, 'r') as reader:
				return Object.valueOf(json.load(reader))
		except Exception:
			return Object()
	@staticmethod
	def string(content):
		try:
			return json.loads(content)
		except Exception:
			return Object()
	
	@staticmethod
	def stringify(*args, **kws):
		return json.dumps(*args, **kws)