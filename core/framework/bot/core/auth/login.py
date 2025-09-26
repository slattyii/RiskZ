from core.framework.bot.core.auth.authcache import LoginCache
from core.framework.bot.core.consts.zlenpoints import LoginEndpoints
from core.system.events.emitter import Emitter
from core.system.logging.log import Log
from core.system.time.date import Timer
from core.system.types.codes import ExitCode, ReturnCode

class LoginState(Emitter):
	def __init__(self, state):
		super().__init__()
		
		self._state = state
		
		self._session = self._state._session
		self._credentialmanager = self._state._credentialmanager
		
		self._cache = LoginCache(self._state)
		
		self._data = None
		self._credential = None
	
	def login(self, name, retry = 0):
		credential = self._credentialmanager.load(name)
		if not credential:
			Log.error(f'no credential named {name!r}', self._state.DEBUG_TAG)
			
			self.emit('login-fail')
			return ReturnCode.ERROR
		
		self._credential = credential

		if not self._cache.isCached(credential.imei):
			payload = {
				'params': {
					'imei': credential.imei,
					'type': '30',
					'client_version': '645',
					'computer_name': 'Web',
					'ts': str(Timer.timestampms())
				},
				'cookies': credential.cookies
			}
			data = self._session._requester.get(
				LoginEndpoints.RISK_ZALO_LOGIN_API_URL,
				**payload
			).parse()
			
			if data.error_code != 0:
				Log.error((data.error_message or 'authenticate failed').lower(), self._state.DEBUG_TAG)
				if self._cache.isCached(credential.imei):
					self._cache.delCache(credential.imei)
				
				if retry == 0:
					return self.login(name, retry = 1)
				
				self.emit('login-fail')
				return ExitCode.ERREXIT
			
			self._data = data.data
		else:
			Log.info('login cache found', self._state.DEBUG_TAG)
			self._data = self._cache.getCache(credential.imei)
		
		self._session._requester.update_cookies(credential.cookies)
		self._cache.setCache(credential.imei, self._data)
		
		self.emit('login-success')
		return ReturnCode.OK