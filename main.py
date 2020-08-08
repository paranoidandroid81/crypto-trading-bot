import trade_bot
import bot_state
import api_client

secret_key = ''
with open('secret_key.txt') as sk:
  secret_key = sk.readline().strip()  
print(secret_key)
api_url = 'https://api.binance.com'
bot = trade_bot.TradeBot(bot_state.BotState().BUY, "BTC", api_client.BinanceApiClient('8xcO7JBozOrVe4RFBTq6aBDsc51C7qyOevh1E1lg3Lo8uTmg3J6qBcOJXWhiEKBM', secret_key, api_url))
print(bot.funds['balances'][0])