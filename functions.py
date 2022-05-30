from Secret import Constants
from binance import Client
from datetime import datetime
client = Client(Constants.api_key, Constants.api_secret)


def ma_trade_logic(pair):
    bar_list = client.get_historical_klines(pair, Client.KLINE_INTERVAL_5MINUTE, "1 day ago UTC")
    return [float(i[4]) for i in bar_list]  # list of pos[4] (is closing price) per time period, also str to float


def ma(input_list, length):
    input_list = input_list[:-1]  # pop off last (=incomplete) time-period
    short_list = input_list[-length::]  # shorten list to requested length
    try:
        result = sum(short_list)/len(short_list)
    except Exception as e:
        print(e)
        result = 0
    return result


def log(log_list):
    final_string = ",".join(log_list)
    try:
        open('Secret/log.csv')
    except FileNotFoundError:
        with open('Secret/log.csv', 'w') as g:
            g.write("Action," +
                    "Pair," +
                    "Balances ALTcoin," +
                    "Altcoin price," +
                    "MA_6h," +
                    "MA_18h," +
                    "Buy amount," +
                    "balance BASE_coin," +
                    "datetime\n")
            g.close()
    with open('Secret/log.csv', 'a') as f:
        f.write(final_string + '\n')
        f.close()
    return


def buy_sell_action_log(stringer):
    try:
        open('Secret/action.csv')
    except FileNotFoundError:
        with open('Secret/action.csv', 'w') as g:
            g.write('Action,' +
                    'Pair,' +
                    'Altcoin price,' +
                    'Quantity,' +
                    'DateTime,' +
                    'Error\n')
            g.close()
    with open('Secret/action.csv', 'a') as f:
        f.write(stringer + '\n')
        f.close()
    return


def error_log(stringer):
    try:
        open('Secret/error.csv')
    except FileNotFoundError:
        with open('Secret/error.csv', 'w') as g:
            g.write('Action,' +
                    'Pair,' +
                    'Error,' +
                    'DateTime\n')
            g.close()
    with open('Secret/error.csv', 'a') as f:
        f.write(stringer + '\n')
        f.close()
    return


def buy(pair, buy_amount, altcoin_price):
    try:
        buy_order = client.order_market_buy(symbol=pair, quoteOrderQty=buy_amount)
        buy_sell_action_log(f'Buy,{pair},{altcoin_price},BASEcoin {buy_amount},{datetime.now()},none')
        print('Action = Buy')
        return 'Buy'
    except Exception as e:
        error_log(f'Buy failed in function,{pair},{e},{datetime.now()}')
        print(f'Buy failed - {e}')
        return f'Buy failed - {e}'


def sell(pair, balance_altcoin, altcoin_price):
    try:
        sell_order = client.order_market_sell(symbol=pair, quantity=balance_altcoin)
        buy_sell_action_log(f'Sell,{pair},{altcoin_price},ALTcoin {balance_altcoin},{datetime.now()},none')
        print('Action = Sell')
        return 'Sell'
    except Exception as e:
        error_log(f'Sell failed in function,{pair},{e},{datetime.now()}')
        print(f'Sell failed - {e}')
        return f'Sell failed - {e}'
