from core.system.logging.log import Log
from core.system.time.systemtime import SystemTime

class SystemServer:
	def __init__(self, context):
		self._context = context

		self._systemtime = SystemTime(self)
		
		self.init()
	
	# System Methods
	def _sysinit(self):
		return
	def _sysboot(self):
		self._systemtime.record_boot()
		Log.info(f'system boot')
		Log.info('slatt tired code :D')
	def _sysexit(self, code):
		self._systemtime.record_exit()
		Log.info(f'system exit with code {code}')
	
	def init(self):
		self._init_events()
	def _init_events(self):
		self._context.on(
			'init',
			self._sysinit
		)
		self._context.on(
			'boot',
			self._sysboot
		)
		self._context.on(
			'exit',
			self._sysexit
		)