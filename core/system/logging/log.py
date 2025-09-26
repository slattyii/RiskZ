from core.system.time.date import datetime

DEBUGT = 'DEBUG'
INFOT = 'INFO'
WARNT = 'WARN'
ERORT = 'ERROR'
SUCCT = 'OK'


DEBUG_LABEL = f'\x1b[1;37m{DEBUGT:<8}\x1b[0m'
INFO_LABEL = f'\x1b[1;34m{INFOT:<8}\x1b[0m'
WARNING_LABEL = f'\x1b[1;33m{WARNT:<8}\x1b[0m'
ERROR_LABEL = f'\x1b[1;31m{ERORT:<8}\x1b[0m'
SUCCESS_LABEL = f'\x1b[1;32m{SUCCT:<8}\x1b[0m'

def build(label, tag, msg):
	tag = tag.strip()[:3] if tag else 'SYS'
	return f'\x1b[1;36m{tag:<3}\x1b[0m {label} \x1b[1;35m{datetime.now():%H:%M:%S}\x1b[0m   {msg}'

class Log:
	@staticmethod
	def debug(msg, tag = None):
		print(build(DEBUG_LABEL, tag, msg))
	@staticmethod
	def info(msg, tag = None):
		print(build(INFO_LABEL, tag, msg))
	@staticmethod
	def warning(msg, tag = None):
		print(build(WARNING_LABEL, tag, msg))
	@staticmethod
	def error(msg, tag = None):
		print(build(ERROR_LABEL, tag, msg))
	@staticmethod
	def success(msg, tag = None):
		print(build(SUCCESS_LABEL, tag, msg))