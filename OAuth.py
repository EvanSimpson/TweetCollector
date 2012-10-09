#OAuth 1.0 authentication for Twitter API v1.1

import time
from hashlib import sha1
import hmac
import binascii
import random
import urllib


class OAuth(Object):
	
	def __init__(url, key, token, csecret, tsecret, data = {}, method = "HMAC-SHA1", version = "1.0"):

		oauth_consumer_key = key
		oauth_nonce = self.generate_nonce(13)
		oauth_signature = self.create_signature(url, data, csecret, tsecret)
		oauth_signature_method = method
		oauth_timestamp = self.create_timestamp()
		oauth_token = token
		oauth_version = version

	def generate_nonce(self, length=8):
    	return ''.join([str(random.randint(0, 9)) for i in range(length)])

	def create_timestamp(self):
		return str(int(time.time())


	def build_param_string(self, data):
		pstr = ""
		dest = dict(data)
		d = {'oauth_consumer_key' : self.percent_encode(self.oauth_consumer_key),
			'oauth_nonce' : self.percent_encode(self.oauth_nonce),
			'oauth_signature_method' : self.percent_encode(self.oauth_signature_method),
			'oauth_timestamp' : self.percent_encode(self.oauth_timestamp),
			'oauth_token' : self.percent_encode(self.oauth_token),
			'oauth_version' : self.percent_encode(self.oauth_version)
			} 
		dest.update(d)
		keys = dest.keys().sort()
		for key in keys:
			pstr += key + '=' + dest[key] + '&'
		return pstr[:-1]



	def create_signature(self, url, data, csecret, tsecret):
		pstr = self.build_param_string(data)
		http = 'POST'
		sig_base = http + '&' + self.percent_encode(url) + '&' + self.percent_encode(pstr)
		sign_key = self.percent_encode(csecret)+'&'+self.percent_encode(tsecret)
		hashed = hmac.new(sign_key, sig_base, sha1)
		return binascii.b2a_base64(hashed.digest())[:-1]



	def percent_encode(self, text):
		return urllib.quote(text, '')

	def build_header(self):
		Head = "OAuth "
		for attr, value in self.__dict__.iteritems():
			Head += self.percent_encode(attr)  + '=' + '"' + self.percent_encode(value) + '", '
		return {'Authorization' : Head[:-2]}



