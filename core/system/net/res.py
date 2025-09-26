import requests

from core.system.types.object import Object


class Response(requests.Response):
	def parse(self):
		try:
			return Object.valueOf(self.json())
		except Exception:
			return Object()