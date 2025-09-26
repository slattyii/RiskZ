from threading import Thread as _Thread, Timer

class Thread(_Thread):
	def start(self):
		return super().start()