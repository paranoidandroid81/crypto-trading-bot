import bot_state as bs
import api_client as ac
from trade_type import *

class TradeBot:
  def __init__(self, init_state: bs.BotState, coin_type, api_client: ac.BinanceApiClient):
    self.state = init_state
    self.coin_type = coin_type
    self.api_client = api_client
    self.funds = self.get_account_funds()
  
  def get_account_funds(self):
    return self.api_client.get_account_info()
  
  def get_current_price(self, symbol: str):
    return self.api_client.get_current_price(symbol)
  
  def place_sell_order(self, quantity, symbol: str):
    return self.api_client.place_sell_order(quantity, symbol, TradeType.MARKET)

  def place_buy_order(self, quantity, symbol: str):
    return self.api_client.place_buy_order(quantity, symbol, TradeType.MARKET)
