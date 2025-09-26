from enum import Enum
from attr import dataclass


@dataclass
class ClientParams:
	VER = str(647)
	TYPE = str(30)
@dataclass
class RequestParams:
	ALL = {
		'zpw_ver': ClientParams.VER,
		'zpw_type': ClientParams.TYPE
	}
@dataclass
class CommandType:
	USER_MESSAGE = 501
	GROUP_MESSAGE = 521

class ChatTypes(Enum):
	USER = 0
	GROUP = 1