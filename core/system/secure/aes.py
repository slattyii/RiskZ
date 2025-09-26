import base64
import json
import gzip
import urllib.parse
import zlib
from Crypto.Cipher import AES as CryptoAES
from Crypto.Util.Padding import pad, unpad

class AES:
	def __init__(self):
		pass

	def _get_key(self, b64key: str, key_size: int = None) -> bytes:
		key = base64.b64decode(b64key)
		if key_size and len(key) != key_size:
			raise ValueError(f"Key must be {key_size} bytes")
		return key

	def _encode(self, b64key: str, data: str, key_size: int) -> str:
		key = self._get_key(b64key, key_size)
		iv = b'\x00' * 16
		cipher = CryptoAES.new(key, CryptoAES.MODE_CBC, iv)
		padded_data = pad(data.encode(), CryptoAES.block_size)
		encrypted = cipher.encrypt(padded_data)
		return base64.b64encode(encrypted).decode()

	def _decode(self, b64key: str, b64data: str, key_size: int) -> str:
		key = self._get_key(b64key, key_size)
		iv = b'\x00' * 16
		cipher = CryptoAES.new(key, CryptoAES.MODE_CBC, iv)
		encrypted_data = base64.b64decode(b64data)
		decrypted = unpad(cipher.decrypt(encrypted_data), CryptoAES.block_size)
		return decrypted.decode()

	def encode128(self, b64key: str, data: str) -> str:
		return self._encode(b64key, data, 16)

	def decode128(self, b64key: str, b64data: str) -> str:
		return self._decode(b64key, b64data, 16)

	def encode256(self, b64key: str, data: str) -> str:
		return self._encode(b64key, data, 32)

	def decode256(self, b64key: str, b64data: str) -> str:
		return self._decode(b64key, b64data, 32)

	def gcm_decrypt(self, b64key: str, b64data: str) -> str:
		raw = base64.b64decode(b64data)
		if len(raw) < 48:
			raise ValueError("Invalid GCM payload")
		iv = raw[:16]
		aad = raw[16:32]
		data = raw[32:]
		if len(data) < 16:
			raise ValueError("Missing tag")
		ciphertext = data[:-16]
		tag = data[-16:]
		key = self._get_key(b64key)
		cipher = CryptoAES.new(key, CryptoAES.MODE_GCM, nonce=iv)
		cipher.update(aad)
		decrypted = cipher.decrypt_and_verify(ciphertext, tag)
		return decrypted.decode()

	def wsdecode(self, payload, encrypt_type, key):
		if not payload or not key:
			return None
		try:
			if encrypt_type == 0:
				decoded_data = payload
			elif encrypt_type == 1:
				decrypted_data = base64.b64decode(payload)
				decompressed_data = gzip.decompress(decrypted_data)
				decoded_data = decompressed_data.decode("utf-8")
			elif encrypt_type == 2:
				data_bytes = base64.b64decode(urllib.parse.unquote(payload))
				if len(data_bytes) < 48:
					return None
				iv = data_bytes[:16]
				aad = data_bytes[16:32]
				cipher_data = data_bytes[32:]
				if len(cipher_data) < 16:
					return None
				ciphertext = cipher_data[:-16]
				tag = cipher_data[-16:]
				aes_key = self._get_key(key)
				cipher = CryptoAES.new(aes_key, CryptoAES.MODE_GCM, nonce=iv)
				cipher.update(aad)
				decrypted = cipher.decrypt_and_verify(ciphertext, tag)
				decompressed = zlib.decompress(decrypted, wbits=16)
				decoded_data = decompressed.decode("utf-8")
			else:
				return None
			return json.loads(decoded_data)
		except Exception as e:
			raise Exception(f"Unable to decode payload! Error: {e}")