from Secret import Constants
from Calculations import ma_trade_logic, ma, log, buy_sell_action_log
from binance import Client
from datetime import datetime
import sys

# Command Line Argument
arg_list = sys.argv
symbol_altcoin_list = []  # Default ALT coin list

if len(arg_list) > 1:
    symbol_altcoin_list = []
    for i in range(1, len(arg_list) - 1):
        symbol_altcoin_list.append(arg_list[i])
    symbol_basecoin = str(arg_list[-1])
else:
    symbol_altcoin_list = ['SOL', 'MANA', 'ETH']  # Default ALT coin list
    symbol_basecoin = 'BUSD'

pairs = []  # creating pairs list, ALT-BASE pair
for i in range(0, len(symbol_altcoin_list)):
    pairs.append(str(symbol_altcoin_list[i]) + symbol_basecoin)

# open connection with api, collect coins data
client = Client(Constants.api_key, Constants.api_secret)

# multiple closing lists for each pair
closing_list = []

for i in range(0, len(pairs)):
    closing_list.append(ma_trade_logic(
        client.get_historical_klines(pairs[i], Client.KLINE_INTERVAL_5MINUTE, "1 day ago UTC")))

# BNB, BUSD, basecoin and altcoin free balance
balance_BNB_dict = client.get_asset_balance(asset='BNB')
balance_BNB = float(balance_BNB_dict['free'])
balance_BUSD_dict = client.get_asset_balance(asset='BUSD')
balance_BUSD = float(balance_BUSD_dict['free'])

# # for i in range(0, len(pairs)):
#     balance_basecoin_dict = client.get_asset_balance(asset=symbol_basecoin)
#     balance_basecoin = float(balance_basecoin_dict['free'])
#     balance_alt_dict = client.get_asset_balance(asset=symbol_altcoin1)
#     balance_altcoin = float(balance_alt_dict['free'])
# #
# # ALT-BASE price
# prices = client.get_all_tickers()
# altcoin_price = 100000000000000000000  # alternative price
# for each in prices:
#     if each['symbol'] == pair:
#         altcoin_price = float(each['price'])
#
# # Determine the MA's
# ma_6 = round(ma(closing_list, 12 * 6), 8)  # use 12* (6 hours) b.o. 5min interval
# ma_18 = round(ma(closing_list, 12 * 18), 8)  # use 12 * (18 hours) b.o. 5min interval
# print(f'MA-6 {pair}: {ma_6}')
# print(f'MA-18 {pair}: {ma_18}')
#
# # Buy or Sell? that's the question
# log_list = []
# buy_amount = int(0)
# if (ma_6 >= ma_18) & (balance_altcoin == 0) & (balance_basecoin != 0):  # Buy order
#     try:
#         buy_amount = int(0.99 * balance_basecoin)  # amount of BASEcoin to spend, ie 99%
#         buy_order = client.order_market_buy(symbol=pair, quoteOrderQty=buy_amount)
#         log_list.append('Buy')
#         buy_sell_action_log(f'Buy,{pair},{altcoin_price},BASEcoin {buy_amount},{datetime.now()},none')
#         print('Action = Buy')
#     except Exception as e:
#         buy_sell_action_log(f'Buy failed,{pair},{altcoin_price},BASEcoin {buy_amount},{datetime.now()},{e}')
#         log_list.append(f'Buy failed - {e}')
#         print(f'Buy failed - {e}')
#
# elif (ma_6 < ma_18) & (balance_altcoin != 0):  # sell order
#     try:
#         sell_order = client.order_market_sell(symbol=pair, quantity=balance_altcoin)
#         log_list.append('Sell')
#         buy_sell_action_log(f'Sell,{pair},{altcoin_price},ALTcoin {balance_altcoin},{datetime.now()},none')
#         print('Action = Sell')
#     except Exception as e:
#         buy_sell_action_log(f'Sell failed,{pair},{altcoin_price},ALTcoin {balance_altcoin},{datetime.now()},{e}')
#         log_list.append(f'Sell failed - {e}')
#         print(f'Sell failed - {e}')
#
# else:
#     log_list.append('No action')
#     print('Action = Do nothing')
#
# # register all the action
# log_list.append(str(symbol_altcoin1))
# log_list.append(str(symbol_basecoin))
# log_list.append(str(buy_amount))
# log_list.append(str(altcoin_price))
# log_list.append(str(ma_6))
# log_list.append(str(ma_18))
# log_list.append(str(balance_altcoin))
# log_list.append(str(balance_basecoin))
# log_list.append(str(datetime.now()))
# log(log_list)
#
#
# #  adding BNB to balance
# BNB_log_list = []
# if (balance_BNB < 0.1) & (balance_BUSD > 10):
#     try:
#         buy_order = client.order_market_buy(symbol='BNBBUSD', quoteOrderQty=10)
#         buy_sell_action_log(f'Buy-BNB,BNBBUSD,na,na,{datetime.now()},none')
#         BNB_log_list.append('Buy BNB')
#         print('Action = Buy BNB')
#     except Exception as e:
#         buy_sell_action_log(f'Buy-BNB failed,BNBBUSD,na,na,{datetime.now()},{e}')
#         BNB_log_list.append('Buy failed BNB')
#         print(f'Buy-BNB failed - {e}')
# else:
#     BNB_log_list.append('Didn\'t buy BNB')
#     print('Action = Didn\'t buy BNB')
#
# BNB_log_list.append('BNB')
# BNB_log_list.append('BUSD')
# BNB_log_list.append('na')
# BNB_log_list.append('na')
# BNB_log_list.append('na')
# BNB_log_list.append('na')
# BNB_log_list.append(str(balance_BNB))
# BNB_log_list.append(str(balance_BUSD))
# BNB_log_list.append(str(datetime.now()))
# log(BNB_log_list)
