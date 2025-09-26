from core.system.filesystem.fs import FSContext

class CacheFS(FSContext):
	def __init__(self, context):
		self._context = context
		self._rootfs = self._context._rootfs
		
		super().__init__(self._rootfs.relative, 'cache')