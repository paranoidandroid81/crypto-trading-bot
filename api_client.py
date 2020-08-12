import requests
import hmac
import hashlib
import time
from trade_type import *
import decimal as dec

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
    headers = {'X-MBX-APIKEY': self.api_key}
    reply = requests.get(f'{self.api_url}/api/v3/account', params=query_params, headers=headers)
    return reply.json()
  
  def get_signature_from_query_dict(self, query_params: dict):
    all_params = list(map(lambda param: f'{param[0]}={param[1]}', query_params.items()))
    param_string = '&'.join(all_params).strip()
    secret_key_bytes = self.secret_key.encode('utf-8')
    hmac_result = hmac.new(secret_key_bytes, param_string.encode('utf-8'), hashlib.sha256).hexdigest()
    return hmac_result

  def get_current_price(self, symbol: str):
    query_params = {}
    query_params['symbol'] = symbol
    print(symbol)
    headers = {'X-MBX-APIKEY': self.api_key}
    reply = requests.get(f'{self.api_url}/api/v3/avgPrice', params=query_params, headers=headers)
    return reply.json()
  
  def place_sell_order(self, quantity: dec.Decimal, symbol: str, trade_type: TradeType):
    query_params = self.form_order_request(quantity, symbol, trade_type, 'SELL')
    query_params['timestamp'] = current_milli_time()
    query_params['signature'] = self.get_signature_from_query_dict(query_params)
    headers = {'X-MBX-APIKEY': self.api_key}
    reply = requests.post(f'{self.api_url}/api/v3/order', params=query_params, headers=headers)
    return reply.json()

  @staticmethod
  def form_order_request(quantity: dec.Decimal, symbol: str, trade_type: TradeType, side: str):
    query_params = {}
    query_params['symbol'] = symbol
    query_params['quantity'] = quantity
    query_params['side'] = side
    query_params['type'] = str(trade_type)
    return query_params
  
  def place_buy_order(self, quantity: dec.Decimal, symbol: str, trade_type: TradeType):
    query_params = self.form_order_request(quantity, symbol, trade_type, 'BUY')
    query_params['timestamp'] = current_milli_time()
    query_params['signature'] = self.get_signature_from_query_dict(query_params)
    headers = {'X-MBX-APIKEY': self.api_key}
    reply = requests.post(f'{self.api_url}/api/v3/order', params=query_params, headers=headers)
    return reply.json()

