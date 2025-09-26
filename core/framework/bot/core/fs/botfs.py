from core.system.filesystem.fs import FSContext
from core.system.logging.log import Log

class BotFS(FSContext):
	def __init__(self, state):
		self._state = state
		self._rootfs = self._state._context._rootfs

		self._bot_folder_name = 'bot'

		if not self._rootfs.exists(self._rootfs.path(self._bot_folder_name)):
			Log.warning('first run detected! please check and add necessary data for future runs', self._state.DEBUG_TAG)
		
		super().__init__(self._rootfs.relative, self._bot_folder_name)