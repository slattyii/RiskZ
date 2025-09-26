import os as _os
import sys as _sys
import shutil as _shutil
from pathlib import Path as _Path

from core.system.filesystem.conf import PROJECT_ROOT

class FSContext: 
	def __init__(self, base, name):
		self.base = _Path(base).resolve()
		self.name = name
		self.relative = self.base / self.name

		self.ensure()

	### Important Methods ###
	############################################################################
	def ensure(self):
		if not self.base.exists():
			self.base.mkdir(parents=True, exist_ok=True)
		if not self.relative.exists():
			self.relative.mkdir(parents=True, exist_ok=True)
	def wipe(self):
		if not self.exists(self.relative):
			return
		
		_shutil.rmtree(self.relative)
		self.ensure()
	
	### Path Methods ###
	############################################################################
	def path(self, *paths):
		return self.relative.joinpath(*paths).resolve()
	
	### Context Methods ###
	############################################################################
	def child(self, name):
		return FSContext(self.relative, name)

	### File Methods ###
	############################################################################
	def exists(self, path):
		return _os.path.exists(path)
	def readdir(self, path = None):
		if not path:
			path = str(self.relative)
		if not self.exists(path):
			return []
		
		return _os.listdir(path)
	def mapdir(self, path):
		return list(map(
			lambda x: _Path(path) / _Path(x),
			self.readdir(path)
		))
	def delete(self, path):
		return _os.remove(path)

ProjectFS = FSContext(PROJECT_ROOT, '/')