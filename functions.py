from Secret import Constants
from binance import Client
from datetime import datetime
client = Client(Constants.api_key, Constants.api_secret)


def balance(symbol: str):
    return float(client.get_asset_balance(asset=symbol)['free'])


def price(coin_pair: str):
    return float(client.get_ticker(symbol=coin_pair)['lastPrice'])


def ma(pair: str, ma_a: int, ma_b: int, interval: str):
    interval_choices = {
        '1m': 'Client.KLINE_INTERVAL_1MINUTE',
        '3m': 'Client.KLINE_INTERVAL_3MINUTE',
        '5m': 'Client.KLINE_INTERVAL_5MINUTE',
        '15m': 'Client.KLINE_INTERVAL_15MINUTE',
        '30m': 'Client.KLINE_INTERVAL_30MINUTE',
        '1h': 'Client.KLINE_INTERVAL_1HOUR',
        '2h': 'Client.KLINE_INTERVAL_2HOUR',
        '4h': 'Client.KLINE_INTERVAL_4HOUR',
        '6h': 'Client.KLINE_INTERVAL_6HOUR',
        '8h': 'Client.KLINE_INTERVAL_8HOUR',
        '12h': 'Client.KLINE_INTERVAL_12HOUR',
        '1d': 'Client.KLINE_INTERVAL_1DAY',
        '3d': 'Client.KLINE_INTERVAL_3DAY',
        '1w': 'Client.KLINE_INTERVAL_1WEEK',
        '1M': 'Client.KLINE_INTERVAL_1MONTH'
    }
    inter = interval_choices[interval]
    input_list = [float(i[4]) for i in client.get_historical_klines(pair, Client.KLINE_INTERVAL_15MINUTE, "1 day ago UTC")]
    input_list = input_list[:-1]
    short_list_a = input_list[-ma_a::]  # shorten list to requested length
    short_list_b = input_list[-ma_b::]  # shorten list to requested length

    try:
        result_a = round(sum(short_list_a)/len(short_list_a), 4)
    except Exception as e:
        print(e)
        result_a = 0
    try:
        result_b = round(sum(short_list_b) / len(short_list_b), 4)
    except Exception as e:
        print(e)
        result_b = 0
    return result_a, result_b


def fraction_basecoin(pairs: dict, balance_BASEcoin: float, balance_ALTcoins: dict):
    pair_count = len(pairs)
    buy_amount = 0
    if (balance_BASEcoin > 10) & (pair_count > 0):
        for coin in balance_ALTcoins:
            if balance_ALTcoins[coin] != 0:
                pair_count -= 1
        try:
            buy_amount = int(balance_BASEcoin / pair_count)
        except Exception as e:
            print(e)
    return buy_amount


def buy_sell_action(action: str, pair: str, amount, price: float):
    if action.upper() == 'BUY':
        try:
            client.order_market_buy(symbol=pair, quoteOrderQty=amount)
            log(f'Buy,{pair},{amount},{price},none', 'log')
            log(f'Buy,{pair},{amount},{price},none', 'action')
            return f'Action = Buy {pair}'
        except Exception as e:
            log(f'Buy failed,{pair},{amount},{price},{e}', 'log')
            log(f'Buy failed,{pair},{amount},{price},{e}', 'error')
            return f'Buy failed - {pair} - {e}'
    elif action.upper() == 'SELL':
        try:
            client.order_market_sell(symbol=pair, quantity=amount)
            log(f'Sell,{pair},{amount},{price},none', 'log')
            log(f'Sell,{pair},{amount},{price},none', 'action')
            return f'Action = Sell {pair}'
        except Exception as e:
            log(f'Sell failed,{pair},{amount},{price},{e}', 'log')
            log(f'Sell failed,{pair},{amount},{price},{e}', 'error')
            return f'Sell failed - {pair} - {e}'


def log(stringer: str, name: str):
    file = f'{name}.csv'
    try:
        open(file)
    except FileNotFoundError:
        with open(file, 'w') as g:
            g.write("Action," +
                    "Pair," +
                    "Quantity," +
                    "Price," +
                    "Error," +
                    "datetime" +
                    "\n")
            g.close()
    with open(file, 'a') as f:
        f.write(stringer + f',{datetime.now()}\n')
        f.close()
    return
