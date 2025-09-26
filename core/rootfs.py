from core.system.filesystem.fs import FSContext
from core.system.filesystem.conf import PROJECT_ROOT

class RootFS(FSContext):
	def __init__(self, context):
		super().__init__(PROJECT_ROOT, 'root')
	
		self._context = context