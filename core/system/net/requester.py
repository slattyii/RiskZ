from requests import Session

from core.system.net.res import Response
from core.system.types.json import Rson
from core.system.types.object import Object

class Requester(Session):
	def __init__(
		self,
		headers = None,
		cookies = None,
		proxies = None,
		*args,
		**kws
	):
		super().__init__(*args, **kws)
		
		self._useragent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
		self.__configs = {
			'headers': self.validate_headers(headers),
			'cookies': self.validate_cookies(cookies),
			'proxies': self.validate_proxies(proxies),
		}

	def validate_dict(self, obj):
		if not isinstance(obj, dict):
			return {}
		return obj
	def validate_headers(self, headers):
		headers = self.validate_dict(headers)
		
		return self.merge_obj(self.get_default_headers(), headers)
	def validate_cookies(self, cookies):
		return self.validate_dict(cookies)
	def validate_proxies(self, proxies):
		if proxies == 'auto':
			return self.get_default_proxies()
		elif isinstance(proxies, dict):
			return proxies
		
		return self.validate_dict(proxies)
	
	def merge_obj(self, r, t):
		return (r | t)
	def merge_headers(self, headers = None):
		headers = self.validate_dict(headers)
		
		return self.merge_obj(self.__configs['headers'], headers)
	def merge_cookies(self, cookies = None):
		cookies = self.validate_dict(cookies)
		
		return self.merge_obj(self.__configs['cookies'], cookies)
	def merge_proxies(self, proxies = None):
		proxies = self.validate_dict(proxies)
		
		return self.merge_obj(self.__configs['proxies'], proxies)
	
	def set_headers(self, headers):
		headers = self.validate_dict(headers)
		
		self.__configs['headers'] = headers
	def set_cookies(self, cookies):
		cookies = self.validate_dict(cookies)
		
		self.__configs['cookies'] = cookies
	def set_proxies(self, cookies):
		proxies = self.validate_dict(proxies)
		
		self.__configs['proxies'] = proxies
		
	def update_headers(self, headers):
		headers = self.validate_headers(headers)
		
		self.__configs['headers'] = headers
	def update_cookies(self, cookies):
		cookies = self.validate_cookies(cookies)
		
		self.__configs['cookies'] = cookies
	def update_proxies(self, proxies):
		proxies = self.validate_proxies(proxies)
		
		self.__configs['proxies'] = proxies
	
	def get_configs(self):
		return self.__configs
	def get_default_headers(self):
		return {
			'User-Agent': self._useragent
		}
	def get_default_cookies(self):
		return {}
	def get_default_proxies(self):
		return {
			'http': 'socks5h://localhost:9050',
			'https': 'socks5h://localhost:9050'
		}
	
	def request(self, *args, **kws):
		kws['headers'] = self.merge_headers(kws.get('headers'))
		kws['cookies'] = self.merge_cookies(kws.get('cookies'))
		kws['proxies'] = self.merge_proxies(kws.get('proxies'))
		
		if type(kws.get('proxies')) is str:
			kws['proxies'] = self.validate_proxies(kws['proxies'])
		
		try:
			_origin_response = super().request(*args, **kws)
			_response = Response()
			_response.__dict__.update(_origin_response.__dict__)
			
			return _response
		except Exception:
			return Object()

	@property
	def ipv4(self):
		try:
			return self.get('https://api.ipify.org?format=json').data.parse().ip
		except Exception:
			return
	@property
	def ipv6(self):
		try:
			return self.get('https://api64.ipify.org?format=json').data.parse().ip
		except Exception:
			return
	@property
	def ipdns(self):
		try:
			return {
				'ipv4': self.get('https://api.ipify.org?format=json', proxies = 'auto').data.parse().ip,
				'ipv6': self.get('https://api64.ipify.org?format=json', proxies = 'auto').data.parse().ip
			}
		except Exception:
			return {}