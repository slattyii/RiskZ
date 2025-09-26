class Send2MeData:
	def __init__(self, data):
		self._data = data
		
		self.id = self._data.send2me_id

class Zpw:
	def __init__(self, data):
		self._data = data
		
		self.enk = self._data.zpw_enk
		self.wpsk = self._data.zpw_wpsk