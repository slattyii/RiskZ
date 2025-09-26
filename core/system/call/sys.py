import os as _os
import sys as _sys

class SystemCall:
	def __init__(self, context):
		self._context = context
	
	def exit(self, *args, **kws):
		return _sys.exit(*args, *kws)