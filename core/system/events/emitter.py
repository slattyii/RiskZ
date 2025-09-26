class Emitter:
	def __init__(self):
		self.events = {}
	
	def on(self, event, func):
		if event not in self.events:
			self.events[event] = []
		self.events[event].append(func)
	
	def emit(self, event, *args, **kwargs):
		if event in self.events:
			for func in self.events[event]:
				func(*args, **kwargs)