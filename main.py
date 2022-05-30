from Secret import Constants
from functions import ma_trade_logic, ma, log, buy, sell, error_log
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
    symbol_altcoin_list = ['SOL', 'MANA', 'SAND']  # Default ALT coin list
    symbol_basecoin = 'BUSD'

pairs = {}  # creating pairs dict, ALT: ALT-BASE-pair
for each in symbol_altcoin_list:
    pairs[each] = str(each + symbol_basecoin)


# open connection with api, collect coins data
client = Client(Constants.api_key, Constants.api_secret)


# multiple closing-price lists for each pair and ma_6 and ma_18 of each pair
closing_list = {}
ma_6 = {}
ma_18 = {}
for each in symbol_altcoin_list:
    closing_list[pairs[each]] = ma_trade_logic(pairs[each])
    ma_6[pairs[each]] = round(ma(closing_list[pairs[each]], 12 * 6), 8)  # use 12* (6 hours) b.o. 5min interval
    ma_18[pairs[each]] = round(ma(closing_list[pairs[each]], 12 * 18), 8)  # use 12 * (18 hours) b.o. 5min interval


# BNB, BUSD, basecoin and altcoin free balance
balance_BNB_dict = client.get_asset_balance(asset='BNB')
balance_BNB = float(balance_BNB_dict['free'])
balance_BUSD_dict = client.get_asset_balance(asset='BUSD')
balance_BUSD = float(balance_BUSD_dict['free'])
balance_BASEcoin_dict = client.get_asset_balance(asset=symbol_basecoin)
balance_BASEcoin = float(balance_BASEcoin_dict['free'])

balance_ALTcoin_dict = {}
for coin in symbol_altcoin_list:
    balance_ALTcoin_dict[coin] = float(dict(client.get_asset_balance(asset=coin))['free'])


# ALT-BASE price
prices = client.get_all_tickers()
altcoin_price = {}
for each in prices:
    for coin in symbol_altcoin_list:
        if each['symbol'] == pairs[coin]:
            altcoin_price[pairs[coin]] = float(each['price'])

print(f'Pairs: {pairs}')
print(f'Balances: {balance_ALTcoin_dict}')
print(f'Balances: BASEcoin: {balance_BASEcoin}, BNB: {balance_BNB}, BUSD: {balance_BUSD}')
print(f'The ALT-BASEcoin prices: {altcoin_price}')
print(f'MA-6 : {ma_6}')
print(f'MA-18 : {ma_18}')

# fraction of BASEcoin te spend:
pair_count = len(pairs)
buy_amount = 0
if balance_BASEcoin > 10:
    for coin in balance_ALTcoin_dict:
        if balance_ALTcoin_dict[coin] != 0:
            pair_count -= 1
    try:
        buy_amount = int(balance_BASEcoin / pair_count)
    except Exception as e:
        print(e)

    print(f'Buy amount: int({balance_BASEcoin} / {pair_count}) = {buy_amount}')

# Buy or Sell? that's the question

for coin in symbol_altcoin_list:
    log_list = []
    if (ma_6[pairs[coin]] >= ma_18[pairs[coin]]) & (balance_ALTcoin_dict[coin] == 0) & (balance_BASEcoin != 0):
        try:
            log_list.append(buy(pairs[coin], buy_amount, altcoin_price[pairs[coin]]))  # Buy order
        except Exception as e:
            error_log(f'Buy,{pairs[coin]},{e},{datetime.now()}')
    elif (ma_6[pairs[coin]] < ma_18[pairs[coin]]) & (balance_ALTcoin_dict[coin] != 0):
        try:
            log_list.append(sell(pairs[coin], balance_ALTcoin_dict[coin], altcoin_price[pairs[coin]]))  # sell order
        except Exception as e:
            error_log(f'Sell,{pairs[coin]},{e},{datetime.now()}')
    else:
        log_list.append('No action')
        print('Action = Do nothing')

    # register all the action
    log_list.append(str(pairs[coin]))
    log_list.append(str(balance_ALTcoin_dict[coin]))
    log_list.append(str(altcoin_price[pairs[coin]]))
    log_list.append(str(ma_6[pairs[coin]]))
    log_list.append(str(ma_18[pairs[coin]]))
    log_list.append(str(buy_amount))
    log_list.append(str(balance_BASEcoin))
    log_list.append(str(datetime.now()))

    log(log_list)


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
# BNB_log_list.append('na')
# log(BNB_log_list)
