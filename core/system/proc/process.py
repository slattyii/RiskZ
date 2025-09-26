from multiprocessing import Process as _Process

class Process(_Process):
	def start(self):
		return super().start()
	
	def safekill(self):
		try:
			return self.kill()
		except Exception:
			return
	def safeterm(self):
		try:
			return self.terminate()
		except Exception:
			return