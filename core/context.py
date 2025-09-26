from core.system.secure.security import Security
from core.system.systemserver.server import SystemServer
from core.system.proc.monitor import ProcessMonitor

from core.system.events.emitter import Emitter
from core.system.events.syssignal import signal
from core.system.call.sys import SystemCall
from core.system.logging.log import Log
from core.system.types.codes import ExitCode

from core.rootfs import RootFS
from core.procfs import ProcFS
from core.cachefs import CacheFS
from core.tmpfs import TemporaryFS

from core.framework.bot.botinit import RiskBot

class Risk(Emitter):
	def __init__(self):
		super().__init__()
		
		self._systemserver = SystemServer(self)
		self.emit('systemserver-init')

		self.emit('early-init')
		
		self._syscall = SystemCall(self)
		self.emit('syscall-init')

		self._rootfs = RootFS(self)
		self.emit('rootfs-init')
		
		self._procfs = ProcFS(self)
		self.emit('procfs-init')
		
		self._cachefs = CacheFS(self)
		self.emit('cachefs-init')
		
		self._tmpfs = TemporaryFS(self)
		self.emit('tmpfs-init')
		
		self._procmonitor = ProcessMonitor(self)
		self.emit('procmonitor-init')
		
		self.init()
		self.emit('init')
		
		self.emit('boot')
		self.boot()

	# System Methods
	def _sysclean(self):
		self.emit('clean')
		return ExitCode.CLNOK
	def _sysexit(self, code, *args, **kws):
		if not isinstance(code, ExitCode):
			code = ExitCode.UNKEXIT
		
		self.emit('exit', code)
		return self._syscall.exit()
	
	def init(self):
		self._init_state()
		self._init_signal_receiver()
	def _init_state(self):
		self._security = Security(self)
	def _init_signal_receiver(self):
		_exit_signal = lambda *args, **kws: self.end()
		
		signal.signal(signal.SIGTERM, _exit_signal)
		signal.signal(signal.SIGINT, _exit_signal)
	
	def clean(self):
		self._sysclean()
	
	def exit(self, code):
		self._sysexit(code)
	
	def end(self):
		self.clean()
		self.exit(ExitCode.SYSEXIT)
	
	def boot(self):
		def sandbox():
			RiskBot(self)
		sandbox()