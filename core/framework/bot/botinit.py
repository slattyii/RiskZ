from core.system.events.emitter import Emitter
from core.system.logging.log import Log

from core.framework.bot.core.botstate import BotState

class RiskBot(Emitter):
	DEBUG_TAG = 'BOT'
	
	def __init__(self, context):
		super().__init__()
		
		self._context = context
		self.emit('early-init')
		
		self.init()
		self.emit('init')
		
		self.start()
	
	# System Methods
	def _sysexit(self, code):
		return code
	
	def init(self):
		self._init_system_events()
	def _init_system_events(self):
		self._context.on(
			'exit',
			self._sysexit
		)
	
	def start(self):
		BotState(self._context)