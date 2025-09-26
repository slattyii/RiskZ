from enum import Enum

class ExitCode(Enum):
	SYSEXIT = 0
	ERREXIT = -1
	UNKEXIT = -2
	
	CLNOK = 0
	CLNER = -1

class ReturnCode:
	OK = 0
	ERROR = -1