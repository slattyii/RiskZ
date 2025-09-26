from core.framework.bot.core.binders.binderctl import BinderController
from core.framework.bot.core.binders.bind.sysbind import SystemBinder
from core.framework.bot.core.client.wscn import WebsocketConnection
from core.system.events.emitter import Emitter
from core.system.logging.log import Log

class ClientConnection(Emitter):
	def __init__(self, state):
		super().__init__()
		
		self._state = state

		self._wsconnection = WebsocketConnection(self)
		self._binderctl = BinderController(self)
		
		self.init()
	
	def init(self):
		self._init_events()
	def _init_events(self):
		self._wsconnection.on('ws-open', self.wsOpen)
		self._wsconnection.on('ws-close', self.wsClose)
		self._wsconnection.on('ws-error', self.wsError)
		self._wsconnection.on('ws-message', self.wsMessage)
		
		self._wsconnection.on('recv-message', self.onRecvMessage)
		self._wsconnection.on('user-message', self.onUserMessage)
		self._wsconnection.on('group-message', self.onGroupMessage)

		

	def start(self):
		self._binderctl.binder(SystemBinder)

		self._wsconnection.create()
	
	def wsOpen(self):
		Log.info('websocket connection created', self._state.DEBUG_TAG)
	def wsClose(self):
		Log.info('websocket connection closed', self._state.DEBUG_TAG)
		self._state._context.end()
	def wsError(self, error):
		Log.error(f'websocket connection error: {error}', self._state.DEBUG_TAG)
	def wsMessage(self, message):
		Log.info('websocket connection message', self._state.DEBUG_TAG)
		Log.info(message, self._state.DEBUG_TAG)
	
	def onRecvMessage(self, msgobject):
		self._binderctl.notify_message_received(msgobject)
	def onUserMessage(self, msgobject):
		return
	def onGroupMessage(self, msgobject):
		return