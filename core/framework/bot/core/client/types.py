class MessageTypes:
	@staticmethod
	def parse_msg_type(msgType):
		if (msgType == 'webchat'): return 1
		if (msgType == 'chat.voice'): return 31
		if (msgType == 'chat.photo'): return 32
		if (msgType == 'chat.sticker'): return 36
		if (msgType == 'chat.doodle'): return 37
		if (msgType == 'chat.recommended'): return 38
		if (msgType == 'chat.link'): return 38
		if (msgType == 'chat.location.new'): return 43
		if (msgType == 'chat.video.msg'): return 44
		if (msgType == 'share.file'): return 46
		if (msgType == 'chat.gif'): return 49
		
		return 1