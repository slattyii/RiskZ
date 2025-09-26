from core.framework.bot.core.client.messages import MessageObject
from core.system.logging.log import Log
from core.system.types.codes import ReturnCode
from core.system.types.json import Rson


class MessageHandler:
	def __init__(self, wscn):
		self._wscn = wscn

		self._wsdeckey = None
	
	def setkey(self, key):
		self._wsdeckey = key
	
	def handle_message(self, data, cmd):
		if not self._wsdeckey:
			Log.error('decrypt key not set', self._wscn._client._state.DEBUG_TAG)
			return ReturnCode.ERROR
		
		msgs = []
		ev = ''

		if cmd == 501:
			msgs = data.data.msgs or []
			ev = 'user'
		elif msgs == 521:
			msgs = data.data.groupMsgs or []
			ev = 'group'
		else:
			Log.error('invalid data', self._wscn._client._state.DEBUG_TAG)
			return ReturnCode.ERROR

		for msg in msgs:
			msgobject = MessageObject(self._wscn, cmd, msg)

			self._wscn.emit('recv-message', msgobject)
			self._wscn.emit(f'{ev}-message', msgobject)