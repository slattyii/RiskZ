from core.system.secure.aes import AES
from core.system.secure.text import Hash


class Security:
	def __init__(self, context):
		self._context = context
		
		self._aes = AES()
		self._hash = Hash()