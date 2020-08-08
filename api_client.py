import requests
import hmac
import hashlib
import binascii
import time

current_milli_time = lambda: int(round(time.time() * 1000))

class BinanceApiClient:
  def __init__(self, api_key, secret_key, api_url):
    self.api_key = api_key
    self.secret_key = secret_key
    self.api_url = api_url
  
  def get_account_info(self):
    query_params = {}
    query_params['timestamp'] = current_milli_time()
    query_params['signature'] = self.get_signature_from_query_dict(query_params)
    print(query_params)
    headers = {'X-MBX-APIKEY': self.api_key}
    reply = requests.get(f'{self.api_url}/api/v3/account', params=query_params, headers=headers)
    print(reply.url)
    return reply.json()
  
  def get_signature_from_query_dict(self, query_params: dict):
    all_params = []
    for param in query_params.items():
      all_params.append(f'{param[0]}={param[1]}')
    param_string = '&'.join(all_params).strip()
    secret_key_bytes = self.secret_key.encode('utf-8')
    hmac_result = hmac.new(secret_key_bytes, param_string.encode('utf-8'), hashlib.sha256).hexdigest()
    print(hmac_result)
    return hmac_result
