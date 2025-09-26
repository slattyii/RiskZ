from core.system.proc.process import Process
from core.system.proc.thread import Thread, Timer
from core.system.proc.worker import Worker
from core.system.logging.log import Log

class ProcessMonitor:
	DEBUG_TAG = 'PRC'
	
	def __init__(self, context):
		super().__init__()
		
		self._context = context
		
		self.init()
	
	# System Methods
	def _sysexit(self, code):
		Log.info('kill processes and threads', self.DEBUG_TAG)
		
		for process in self._processes:
			process.safeterm()
			process.safekill()
	
	def init(self):
		self._init_state()
		self._init_events()
	def _init_events(self):
		self._context.on(
			'exit',
			self._sysexit
		)
	def _init_state(self):
		self._processes = []
		self._threads   = []
		
		self._worker    = Worker(self)
	
	
	
	def thread(self, *args, **kws):
		try:
			return Thread(*args, **kws)
		except Exception:
			return
	def process(self, *args, **kws):
		try:
			return Process(*args, **kws)
		except Exception:
			return
	
	
	
	@property
	def Timer(self):
		return Timer