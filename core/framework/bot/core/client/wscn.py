import struct
import websocket
from urllib.parse import urlencode, urlparse
from core.framework.bot.core.client.handlers import MessageHandler
from core.framework.bot.core.client.ver import RequestParams
from core.framework.bot.core.net.conf import DEFAULT_PAYLOAD
from core.system.events.emitter import Emitter
from core.system.logging.log import Log
from core.system.time.date import Timer
from core.system.types.json import Rson
from core.system.types.object import Object


class WebsocketConnection(Emitter):
	def __init__(self, client):
		super().__init__()
		
		self._client = client
		self._procmonitor = self._client._state._context._procmonitor

		self._msghandler = MessageHandler(self)
		
		self.isPingIntervalActive = 0
		self.isConnected = 0
		
		self.wsE2EKey = None
		self.wsPingIntervalScheduler = None
		self.wsConnection = None
	
	# System Methods
	def _sysxit(self):
		return
	
	def create(self):
		conn_url = self._client._state._account._loginstate._data.zpw_ws[0]
		conn_params = {
			**RequestParams.ALL
		}
		conn_headers = {
			'Accept-Encoding': 'gzip, deflate, br, zstd',
			'Accept-Language': 'en-US,en;q=0.9',
			'Cache-Control': 'no-cache',
			'Connection': 'Upgrade',
			'Host': urlparse(conn_url).netloc,
			'Origin': 'https://chat.zalo.me',
			'Pragma': 'no-cache',
			'Sec-WebSocket-Extensions': 'permessage-deflate; client_max_window_bits',
			'Sec-WebSocket-Version': '13',
			'Upgrade': 'websocket',
			'User-Agent': DEFAULT_PAYLOAD['headers']['User-Agent'],
			'Cookie': '; '.join(f'{k}={v}' for k, v in self._client._state._account._loginstate._credential.cookies.items())
		}
		
		def pingInterval():
			if not self.isConnected:
				return
			
			payload = {
				'version': 1,
				'cmd': 2,
				'subCmd': 1,
				'data': {'eventId': str(Timer.timestampms())}
			}
			
			enc_data = Rson.stringify(payload["data"]).encode()
			header = struct.pack("<BIB", payload["version"], payload["cmd"], payload["subCmd"])
			data = header + enc_data
			self.wsConnection.send(data, websocket.ABNF.OPCODE_BINARY)
			
			self.wsPingIntervalScheduler = self._procmonitor.Timer(3 * 60, pingInterval)
			self.wsPingIntervalScheduler.start()
			
		def onopen(ws):
			self.isConnected = 1
			self.emit('ws-open')
		def onclose(ws, code, message):
			self.isConnected = 0
			self.isPingIntervalActive = 0
			
			if self.wsPingIntervalScheduler and self.wsPingIntervalScheduler.is_alive():
				self.wsPingIntervalScheduler.cancel()
			
			self.emit('ws-close')
		def onerror(ws, error):
			self.emit('ws-error', str(error).strip() or 'unknown error')
		def onmessage(ws, data):
			if not isinstance(data, bytes): return
			
			enc_header = data[:4]
			ver, cmd, scmd = [enc_header[0], int.from_bytes(enc_header[1:3], 'little'), enc_header[3]]
			
			enc_data = data[4:]
			dec_data = enc_data.decode()
			if not dec_data or 'eventId' in dec_data:
				return
			
			parsed_data = Rson.string(dec_data)
			
			if ver == 1 and cmd == 1 and scmd == 1 and 'key' in parsed_data:
				self.wsE2EKey = parsed_data['key']

				self._msghandler.setkey(self.wsE2EKey)
				
				if self.isPingIntervalActive:
					self.wsPingIntervalScheduler.cancel()
					self.isPingIntervalActive = 0
				
				pingInterval()
				self.isPingIntervalActive = 1
				
				return
		
			if not self.wsE2EKey:
				return onerror(ws, 'decrypt key not found')
			
			parsed_payload = Object.valueOf(self._client._state._context._security._aes.wsdecode(
				parsed_data['data'],
				parsed_data['encrypt'],
				self.wsE2EKey
			))
			
			if ver == 1 and cmd == 3000 and scmd == 0:
				Log.error('another session is running', self._client._state.LOG_TAG)

				return self.wsConnection.close()
			elif ver == 1 and cmd in [501, 521] and scmd == 0:
				return self._msghandler.handle_message(parsed_payload, cmd)
			
			
		
		conn_ws_url = f'{conn_url}?{urlencode(conn_params)}'
		
		self.wsConnection = websocket.WebSocketApp(
			url = conn_ws_url,
			header = conn_headers,
			on_open = onopen,
			on_close = onclose,
			on_error = onerror,
			on_message = onmessage
		)
		self.wsConnection.run_forever()
	def exit(self):
		if self.isConnected and self.wsConnection:
			self.wsConnection.close()