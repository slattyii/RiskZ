from core.system.filesystem.fs import FSContext
from core.system.logging.log import Log
from core.system.types.json import Rson
from core.system.types.object import Object

class CredentialManager(FSContext):
	def __init__(self, state):
		self._state = state
		self._botfs = self._state._botfs

		self._credentials_folder_name = 'credentials'

		super().__init__(self._botfs.relative, self._credentials_folder_name)
	
		if len(self.readdir()) == 0:
			Log.warning('credentials folder is empty', self._state.DEBUG_TAG)
		
	def load(self, name):
		credential = Rson.file(str(self.path(f'{name}.json')))
		
		if isinstance(credential.cookies, list):
			cookies = {}
			
			for cookie in credential.cookies:
				cookies[cookie.name] = cookie.value 
			
			credential.cookies = Object.valueOf(cookies)
		
		return credential