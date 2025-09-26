from core.framework.bot.core.client.reqptr import ClientPointer
from core.system.time.date import Timer
from core.system.types.codes import ReturnCode
from core.system.types.object import Object

class BinderController:
	def __init__(self, client):
		self._client = client
		self._state = self._client._state
		
		self.__binders = {}
	
	def binder(self, _Binder):
		binder = _Binder()
		binder._bindctl_setup(self._state, self._client)

		binder.bind()

		self.__binders[binder.id] = binder
	def notify_message_received(self, msgobject):
		if self._valid_msg(msgobject) is not ReturnCode.OK:
			return ReturnCode.ERROR
		
		cmd, arg = self._split_msg(msgobject.content)
		syncobject = Object.valueOf({
			'pre': {
				'require': cmd
			},
			'message': {
				'text': arg
			}
		})

		msgobject.setsync(syncobject)
		ptr = ClientPointer(self._state, msgobject)

		for binderid in self.__binders:
			if cmd not in self.__binders[binderid]._cmds:
				continue

			self.__binders[binderid]._cmds[cmd](ptr)
	
	def _split_msg(self, content):
		parts = content.split()
		cmd = parts.pop(0)

		return cmd, ' '.join(parts).strip()
	def _valid_msg(self, msgobject):
		if not isinstance(msgobject.content, str):
			return ReturnCode.ERROR

		return ReturnCode.OK

class Binder:
	def __init__(self):
		self.id = str(Timer.timestampms())

		self._cmds = {}
	
	def _bindctl_setup(self, state, client):
		self._cmdpfx = state._botconf.get('cmdpfx')
	def _bindctl_name(self):
		return 'Binder'
	
	def cmdmacro(self, data, part = 1):
		cmd = ' '.join(data.split()[:part]).strip()
		return f'{self._cmdpfx}{cmd}'
	def cmdctl(self, cmd):
		def wrapper(fn):
			self._cmds[cmd] = fn
		return wrapper
	
	def bind(self):
		return ReturnCode.OK