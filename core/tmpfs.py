from core.system.filesystem.fs import FSContext

class TemporaryFS(FSContext):
	def __init__(self, context):
		self._context = context
		self._rootfs = self._context._rootfs
		
		super().__init__(self._rootfs.relative, 'tmp')
		
		self.init()
	
	# System Methods
	def _sysexit(self, code):
		self.wipe()
	
	def init(self):
		self._init_events()
	def _init_events(self):
		self._context.on(
			'exit',
			self._sysexit
		)