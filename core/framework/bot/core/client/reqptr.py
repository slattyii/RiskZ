from unittest import result
from core.framework.bot.core.client.messages import MessageContent
from core.framework.bot.core.client.types import MessageTypes
from core.framework.bot.core.client.ver import ChatTypes, RequestParams
from core.framework.bot.core.consts.zlenpoints import MessageEndpoints
from core.system.time.date import Timer
from core.system.types.json import Rson
from core.system.types.object import Object


class ClientPointer:
	def __init__(self, state, msgobject):
		self._state = state
		self._msgobject = msgobject

		self._security = self._state._context._security

		self.message = self._msgobject
	
	@property
	def requester(self):
		return self._state._session._requester
	@property
	def imei(self):
		return self._state._account.imei
	@property
	def zpw(self):
		return self._state._account.zpw
	
	def new_client_id(self):
		return str(Timer.timestampms())
	
	def mkencode(self, data):
		return self._security._aes.encode128(self.zpw.enk, data)
	def mkdecode(self, data):
		try:
			return Object.valueOf(Rson.string(self._security._aes.decode128(self.zpw.enk, data)))
		except Exception:
			return Object()
	def mkrequest(self, method, endp, opts):
		result = getattr(self.requester, method)(endp, **opts)
		data = result.parse()

		if data.error_code == 0 and data.data:
			data = self.mkdecode(data.data)

			return data
		return data


	
	def sendTo(self, content, chat_id, chat_type,  ttl = 0):
		payload = {
			'params': {
				'message': str(content.text),
				'imei': self.imei,
				'clientId': self.new_client_id(),
				'ttl': ttl
			}
		}

		if content.style:
			payload['params']['textProperties'] = content.style

		if chat_type is ChatTypes.USER:
			endp = MessageEndpoints.RISK_ZALO_USERSMS_API_URL
			payload['params']['toid'] = str(chat_id)
		elif chat_type is ChatTypes.GROUP:
			endp = MessageEndpoints.RISK_ZALO_GROUPSMS_API_URL
			payload['params']['visibility'] = 0
			payload['params']['grid'] = str(chat_id)
		else:
			return
		
		payload['params'] = self.mkencode(Rson.stringify(payload['params']))
		data = self.mkrequest('post', endp, {
			'params': RequestParams.ALL,
			'data': payload
		})

		return data.data or data
	def send(self, content, ttl = 0):
		content = content if isinstance(content, MessageContent) else MessageContent(content)

		return self.sendTo(
			content = content,
			chat_id = self._msgobject.chat.id,
			chat_type = self._msgobject.chat.type,
			ttl = 0
		)
	
	def replyTo(self, message, content, chat_id, chat_type,  ttl = 0):
		payload = {
			'params': {
				'message': content.text,
				'clientId': self.new_client_id(),
				'qmsgOwner': str(int(message.uidFrom) or self._state._account.uid),
				'qmsgId': message.msgId,
				'qmsgCliId': message.cliMsgId,
				'qmsgType': MessageTypes.parse_msg_type(message.msgType),
				'qmsg': message.content,
				'qmsgTs': message.ts,
				'qmsgAttach': Rson.stringify({}),
				'qmsgTTL': 0,
				'ttl': ttl,
			}
		}

		if content.style:
			payload['params']['textProperties'] = content.style

		if chat_type is ChatTypes.USER:
			endp = MessageEndpoints.RISK_ZALO_USERQUOTE_API_URL
			payload['params']['toid'] = str(chat_id)
		elif chat_type is ChatTypes.GROUP:
			endp = MessageEndpoints.RISK_ZALO_GROUPQUOTE_API_URL
			payload['params']['visibility'] = 0
			payload['params']['grid'] = str(chat_id)
		else:
			return
		
		payload['params'] = self.mkencode(Rson.stringify(payload['params']))
		data = self.mkrequest('post', endp, {
			'params': RequestParams.ALL,
			'data': payload
		})

		return data.data or data
	def reply(self, content, ttl = 0):
		content = content if isinstance(content, MessageContent) else MessageContent(content)

		return self.replyTo(
			message = self._msgobject.obj,
			content = content,
			chat_id = self._msgobject.chat.id,
			chat_type = self._msgobject.chat.type,
			ttl = 0
		)