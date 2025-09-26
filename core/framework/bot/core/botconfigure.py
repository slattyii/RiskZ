from core.system.filesystem.fs import FSContext
from core.system.types.json import Rson


class BotConfigure(FSContext):
	def __init__(self, state):
		self._state = state
		self._botfs = self._state._botfs

		super().__init__(self._botfs.relative, 'configures')

		self.init()
	
	def init(self):
		self._init_state()
		self._init_fs()
		self._load()
	def _init_state(self):
		self._dflconf_fname = '_dflconf.json'
		self._dflconf_fpath = self.path(self._dflconf_fname)

		self._dflconf = {}
	def _init_fs(self):
		if not self.exists(self._dflconf_fpath):
			return self._writef(Rson.stringify({ 'cmdpfx': '&' }), self._dflconf_fpath)
	def _load(self):
		self._dflconf = Rson.file(self._dflconf_fpath)
	
	def _writef(self, data, path):
		with open(path, 'w') as writer:
			writer.write(data)
	
	def get(self, *args, **kws):
		return self._dflconf.get(*args, **kws)