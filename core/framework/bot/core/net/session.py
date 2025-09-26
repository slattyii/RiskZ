from core.system.net.requester import Requester
from core.framework.bot.core.net.conf import DEFAULT_PAYLOAD

class Session:
	def __init__(self, state):
		self._state = state
		self._requester = Requester(
			**DEFAULT_PAYLOAD
		)