from calendar import c
from attr import dataclass


@dataclass
class LoginEndpoints:
	RISK_ZALO_LOGIN_API_URL = 'https://wpa.chat.zalo.me/api/login/getLoginInfo'

@dataclass
class MessageEndpoints:
	RISK_ZALO_USERSMS_API_URL = 'https://tt-chat2-wpa.chat.zalo.me/api/message/sms'
	RISK_ZALO_GROUPSMS_API_URL = 'https://tt-group-wpa.chat.zalo.me/api/group/sendmsg'

	RISK_ZALO_USERQUOTE_API_URL = 'https://tt-chat2-wpa.chat.zalo.me/api/message/quote'
	RISK_ZALO_GROUPQUOTE_API_URL = 'https://tt-group-wpa.chat.zalo.me/api/group/quote'