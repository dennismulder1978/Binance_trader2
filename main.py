import sys
from functions import *


# Command Line Argument
arg_list = sys.argv
symbol_altcoin_list = []  # Default ALT coin list

if len(arg_list) > 1:
    symbol_altcoin_list = []
    for i in range(1, len(arg_list) - 1):
        symbol_altcoin_list.append(arg_list[i])
    symbol_basecoin = str(arg_list[-1])
else:
    symbol_altcoin_list = ['SOL', 'ADA', 'SAND', 'BTC']  # Default ALT coin list
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


# all prices
price_BNBBUSD = price('BNBBUSD')
price_altcoin = {}
for coin in symbol_altcoin_list:
    price_altcoin[pairs[coin]] = price(pairs[coin])


# multiple moving averages of each pair
ma_a = {}
ma_b = {}
for each in symbol_altcoin_list:
    ma_a[pairs[each]], ma_b[pairs[each]] = ma(pairs[each], 3, 12, '15m')


# Output test
print(f'Balance BNB: {balance_BNB}')
print(f'Balance BUSD: {balance_BUSD}')
print(f'Balance BASEcoin: {balance_BASEcoin}')
print(f'Balance ALTcoins: {balance_ALTcoin_dict}')
print(f'Price BNB-BUSD: {price_BNBBUSD}')
print(f'Price ALT-BASEcoins: {price_altcoin}')
print(f'MA_a ALT-BASEcoins: {ma_a}')
print(f'MA_b ALT-BASEcoins: {ma_b}')


# Buy or Sell? that's the question
buy_amount = fraction_basecoin(pairs, balance_BASEcoin, balance_ALTcoin_dict)
print(f'Buy amount: {buy_amount}')

for coin in symbol_altcoin_list:
    if (ma_a[pairs[coin]] > ma_b[pairs[coin]]) & (balance_ALTcoin_dict[coin] == 0) & (balance_BASEcoin != 0):
        print(buy_sell_action('buy', pairs[coin], buy_amount, price_altcoin[pairs[coin]]))
    elif (ma_a[pairs[coin]] < ma_b[pairs[coin]]) & (balance_ALTcoin_dict[coin] != 0):
        print(buy_sell_action('sell', pairs[coin], balance_ALTcoin_dict[coin], price_altcoin[pairs[coin]]))
    else:
        log(f'Nothing,{pairs[coin]},0,{price_altcoin[pairs[coin]]},none', 'log')
        print(f'Action = Do nothing {pairs[coin]}')


#  adding BNB to balance
if (balance_BNB < 0.1) & (balance_BUSD > 10):
    print(buy_sell_action('buy', 'BNBBUSD', 10, price_BNBBUSD))
else:
    log(f'Nothing,BNBBUSD,0,{price_BNBBUSD},none', 'log')
    print('Action = Do nothing BNBBUSD')
