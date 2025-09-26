from core.framework.bot.core.auth.datablocks import Send2MeData, Zpw
from core.framework.bot.core.auth.login import LoginState
from core.system.logging.log import Log

class Account:
	def __init__(self, state):
		self._state = state
		
		self._loginstate = LoginState(self._state)
		
		self.init()
	
	def init(self):
		self._init_events()
	def _init_events(self):
		self._loginstate.on(
			'login-fail',
			self.onLoginFailed
		)
		self._loginstate.on(
			'login-success',
			self.onLoginSuccess
		)
	
	def onLoginFailed(self):
		return
	def onLoginSuccess(self):
		self.imei = self._loginstate._credential.imei
		self.cookies = self._loginstate._credential.cookies

		self.uid = self._loginstate._data.uid
		
		self.send2me = Send2MeData(self._loginstate._data)
		self.zpw     = Zpw(self._loginstate._data)
		
		Log.info(f'logged in {self.uid!r}', self._state.DEBUG_TAG)
		return