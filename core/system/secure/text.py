import hashlib

class Hash:
	def md5(self, data):
		return hashlib.md5(str(data).encode()).hexdigest()