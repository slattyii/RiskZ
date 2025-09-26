from core.system.time.date import datetime

class SystemTime:
	def __init__(self, systemserver):
		self._systemserver = systemserver
		
		self._bootat = None
		self._exitat = None
	
	def record_boot(self):
		self._bootat = datetime.now()
	def record_exit(self):
		self._exitat  = datetime.now()
	
	def bootTimeAsString(self):
		if not self._bootat:
			return ''
		
		return self._bootat.strftime('%H:%M:%S')
	def exitTimeAsString(self):
		if not self._exitat:
			return ''
		
		return self._exitat.strftime('%H:%M:%S')