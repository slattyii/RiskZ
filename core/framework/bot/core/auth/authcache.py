from core.system.filesystem.fs import FSContext
from core.system.logging.log import Log
from core.system.types.codes import ReturnCode
from core.system.types.json import Rson


class LoginCache(FSContext):
	DEBUG_TAG = 'LCC'
	
	def __init__(self, state):
		self._state = state
		self._credentialmanager = self._state._credentialmanager
		
		super().__init__(self._credentialmanager.relative, '.cache')
		
		self._security = self._state._context._security
	
	def filename(self, hashkey):
		return f'{hashkey}.lc'
	def setCache(self, key, data):
		hashkey = self._security._hash.md5(key)
		ccpath = self.path(self.filename(hashkey))
		
		try:
			with open(ccpath, 'w') as writer:
				writer.write(Rson.stringify(data, indent = 2))
			return ReturnCode.OK
		except Exception as err:
			Log.error(err, self.DEBUG_TAG)
			return ReturnCode.ERROR
	def delCache(self, key):
		hashkey = self._security._hash.md5(key)
		if self.isCached(key):
			self.delete(self.path(self.filename(hashkey)))
	def isCached(self, key):
		hashkey = self._security._hash.md5(key)
		
		return self.exists(self.path(self.filename(hashkey)))
	
	def getCache(self, key):
		hashkey = self._security._hash.md5(key)
		
		if self.isCached(key):
			return Rson.file(self.path(self.filename(hashkey)))