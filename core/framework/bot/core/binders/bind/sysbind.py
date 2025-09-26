from core.framework.bot.core.binders.binderctl import Binder


class SystemBinder(Binder):
	def bind(self):
		@self.cmdctl(self.cmdmacro('say'))
		def _(ptr):
			ptr.reply(ptr.message.sync.message.text or 'nothing to say')

		return super().bind()