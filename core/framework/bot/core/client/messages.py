from core.framework.bot.core.client.ver import ChatTypes, CommandType


class MessageObject:
	def __init__(self, wscn, cmd, data):
		self._wscn = wscn
		self._cmd = cmd
		self._data = data

		self._account = self._wscn._client._state._account

		self.author = Author(self)
		self.chat		= Chat(self)
		
		self.id = self._data.msgId
		self.content = self._data.content

		self.mentions = self._data.mentions
		self.replying = self._data.quote
		
		self.obj = self._data
		self.sync = None
	
	def setsync(self, syncobject):
		self.sync = syncobject

class Chat:
	def __init__(self, msgobject):
		self._msgobject = msgobject

		if self._msgobject._cmd == CommandType.USER_MESSAGE:
			self.id = str(int(self._msgobject._data.uidFrom) or self._msgobject._data.idTo)
			self.type = ChatTypes.USER
		elif self._msgobject._cmd == CommandType.GROUP_MESSAGE:
			self.id = str(int(self._msgobject._data.idTo) or self._msgobject._account.uid)
			self.type = ChatTypes.GROUP

class Author:
	def __init__(self, msgobject):
		self._msgobject = msgobject

		self.id = str(int(self._msgobject._data.uidFrom) or self._msgobject._account.uid)

	def is_self(self):
		return self.id == self._msgobject._account.uid



class MessageContent:
	def __init__(self, text, style = None):
		self.text = text
		self.style = style