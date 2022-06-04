import sys
from functions import ma_trade_logic, ma, log, buy, sell, error_log, buy_sell_action_log, balance
from datetime import datetime



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


# BNB, BUSD, basecoin and altcoin free balance
balance_BNB = balance('BNB')
balance_BUSD = balance('BUSD')
balance_BASEcoin = balance(symbol_basecoin)
balance_ALTcoin_dict = {}
for coin in symbol_altcoin_list:
    balance_ALTcoin_dict[coin] = balance(coin)


print(balance_BNB)
print(balance_BUSD)
print(balance_BASEcoin)
for each in balance_ALTcoin_dict:
    print(balance_ALTcoin_dict[each])
# multiple closing-price lists for each pair and ma_6 and ma_18 of each pair

ma_a = {}
ma_b = {}
for each in symbol_altcoin_list:
    ma_a[pairs[each]], ma_b[pairs[each]] = ma(pairs[each], 3, 12)

print(ma_a)
print(ma_b)


# # ALT-BASE price
# prices = client.get_all_tickers()
# altcoin_price = {}
# for each in prices:
#     for coin in symbol_altcoin_list:
#         if each['symbol'] == pairs[coin]:
#             altcoin_price[pairs[coin]] = float(each['price'])

# # fraction of BASEcoin te spend:
# pair_count = len(pairs)
# buy_amount = 0
# if balance_BASEcoin > 10:
#     for coin in balance_ALTcoin_dict:
#         if balance_ALTcoin_dict[coin] != 0:
#             pair_count -= 1
#     try:
#         buy_amount = int(balance_BASEcoin / pair_count)
#     except Exception as e:
#         print(e)
#
#     print(f'Buy amount: int({balance_BASEcoin} / {pair_count}) = {buy_amount}')
#
# # Buy or Sell? that's the question
#
# for coin in symbol_altcoin_list:
#     log_list = []
#     if (ma_a[pairs[coin]] >= ma_b[pairs[coin]]) & (balance_ALTcoin_dict[coin] == 0) & (balance_BASEcoin != 0):
#         try:
#             log_list.append(buy(pairs[coin], buy_amount, altcoin_price[pairs[coin]]))  # Buy order
#         except Exception as e:
#             error_log(f'Buy failed,{pairs[coin]},{e},{datetime.now()}')
#     elif (ma_a[pairs[coin]] < ma_b[pairs[coin]]) & (balance_ALTcoin_dict[coin] != 0):
#         try:
#             log_list.append(sell(pairs[coin], balance_ALTcoin_dict[coin], altcoin_price[pairs[coin]]))  # sell order
#         except Exception as e:
#             error_log(f'Sell failed,{pairs[coin]},{e},{datetime.now()}')
#     else:
#         log_list.append('No action')
#         print('Action = Do nothing')
#
#     # register all the action
#     log_list.append(str(pairs[coin]))
#     log_list.append(str(balance_ALTcoin_dict[coin]))
#     log_list.append(str(altcoin_price[pairs[coin]]))
#     log_list.append(str(ma_a[pairs[coin]]))
#     log_list.append(str(ma_b[pairs[coin]]))
#     log_list.append(str(buy_amount))
#     log_list.append(str(balance_BASEcoin))
#     log_list.append(str(datetime.now()))
#
#     log(log_list)
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
#         error_log(f'Buy failed,BNBBUSD,{e},{datetime.now()}')
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