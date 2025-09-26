from re import LOCALE
from core.framework.bot.core.botconfigure import BotConfigure
from core.framework.bot.core.client.clicn import ClientConnection
from core.system.events.emitter import Emitter
from core.framework.bot.core.net.session import Session
from core.framework.bot.core.auth.account import Account
from core.framework.bot.core.auth.credentials import CredentialManager

from core.framework.bot.core.fs.botfs import BotFS

from core.system.logging.log import Log
from core.system.time.thread import Delay

class BotState(Emitter):
	DEBUG_TAG = 'BOT'
	
	LOGIN_NAME = 'slatt.raw'
	
	def __init__(self, context):
		super().__init__()
		
		self._context = context
		
		self.emit('early-init')
		
		self._botfs = BotFS(self)
		self._botconf = BotConfigure(self)
		
		self._credentialmanager = CredentialManager(self)
		self.emit('credentialmanager-init')
		
		self._session = Session(self)
		self.emit('session-init')
		
		self._account = Account(self)
		self.emit('account-init')
		
		self.init()
		self.start()
	
	# System Methods
	def _sysexit(self, code):
		return 
	
	def init(self):
		self._init_state()
		self._init_events()
	def _init_state(self):
		self._clientconnection = ClientConnection(self)
	def _init_events(self):
		self._context.on(
			'exit',
			self._sysexit
		)
		
		self._account._loginstate.on(
			'login-fail',
			self.onLoginFailed
		)
		self._account._loginstate.on(
			'login-success',
			self.onLoginSuccess
		)
	
	def start(self):
		self._account._loginstate.login(self.LOGIN_NAME)
	
	def onLoginFailed(self):
		return
	def onLoginSuccess(self):
		return self._clientconnection.start()