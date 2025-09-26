from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

class Worker:
	def __init__(self, monitor):
		self._monitor = monitor
		
		self.init()
	
	# System Methods
	def _sysexit(self, code):
		return
	
	def init(self):
		self._init_state()
		self._init_events()
	def _init_events(self):
		self._monitor._context.on(
			'exit',
			self._sysexit
		)
	def _init_state(self):
		self._thread_pool = ThreadPoolExecutor()
		self._process_pool = ProcessPoolExecutor()