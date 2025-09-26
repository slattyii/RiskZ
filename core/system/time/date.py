from datetime import datetime

class Timer:
	@staticmethod
	def timestamp():
		return int(datetime.now().timestamp())
	@staticmethod
	def timestampms():
		return int(datetime.now().timestamp() * 1000)