import argparse
import pandas as pd
import datetime
from collections import deque
import numpy as np
from tqdm import tqdm

from multiprocessing import Pool

import matplotlib
import matplotlib.dates as mdates
matplotlib.use('Agg')
import matplotlib.pyplot as plt  # NOQA


SATOSHI = 10 ** 8


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=str, help="path of candle csv")
    parser.add_argument("output", type=str, help="path of result data")

    # optional argument
    parser.add_argument("--test_iter", type=int, default=1000,
                        help="number of iteration")
    parser.add_argument("--thread_size", type=int, default=8,
                        help="thread size")

    return parser.parse_args()


def judge_orders(wallet, timestamp, low, high):
    remain = deque()
    accepted = deque()
    rejected = deque()

    for order in wallet.orders:
        if timestamp >= order.end:
            rejected.append(order)
        elif timestamp >= order.begin:
            if judge_order(low, high, order):
                accepted.append(order)
            else:
                remain.append(order)
        else:
            remain.append(order)

    wallet.orders = remain

    return accepted, rejected


def judge_order(low, high, order):
    if order.is_buy:
        ret = order.price > low
    else:
        ret = order.price < high
    return ret


def btc2jpy(btc_price, size):
    return btc_price * size // SATOSHI


class Exchange(object):
    def __init__(self):
        self.commition = 0.0015

    def exec_order(self, order, wallet):
        if order.is_buy:
            btc = int(order.size * (1 - self.commition))
            wallet.gain("BTC", btc)
        else:
            jpy = btc2jpy(order.price, int(order.size * (1 - self.commition)))
            wallet.gain("JPY", jpy)


class Wallet(object):
    def __init__(self, jpy, btc):
        self.jpy = jpy
        self.btc = btc

        self.orders = deque()

    def add_order(self, order):
        if order.is_buy:
            self.pay("JPY", btc2jpy(order.price, order.size))
        else:
            self.pay("BTC", order.size)

        self.orders.append(order)

    def cancel_order(self, order):
        if order.is_buy:
            self.gain("JPY", btc2jpy(order.price, order.size))
        else:
            self.gain("BTC", order.size)

    def cancel_orders(self, orders):
        for order in orders:
            self.cancel_order(order)

    def pay(self, type, size):
        if not isinstance(size, int):
            raise TypeError("Size must be integer")

        if type == "JPY":
            self.jpy -= size
        elif type == "BTC":
            self.btc -= size
        else:
            msg = "Currency type must be 'JPY' or 'BTC', but type = {}"
            msg = msg.format(type)
            raise ValueError(msg)

    def gain(self, type, size):
        self.pay(type, -size)

    def __repr__(self):
        s = "jpy: {}\n".format(self.jpy)
        s += "btc: {}\n".format(self.btc / (SATOSHI))
        return s

    def result(self, close):
        tmp_btc = 0
        tmp_jpy = 0
        for order in self.orders:
            if order.is_buy:
                tmp_jpy += btc2jpy(order.price, order.size)
            else:
                tmp_btc += order.size

        return int((self.jpy + tmp_jpy) + btc2jpy(close, (self.btc + tmp_btc)))


class Order(object):
    def __init__(self, side, price, size, begin):
        self.is_buy = (side == "BUY")
        self.price = price
        self.size = size
        self.begin = begin + datetime.timedelta(minutes=1)
        self.end = begin + datetime.timedelta(days=1)

    def __repr__(self):
        s = "[Order]\n"
        s += "is_buy: {}\n".format(self.is_buy)
        s += "price: {}\n".format(self.price)
        s += "size: {}\n".format(self.size / SATOSHI)
        s += "begin: {}\n".format(self.begin)
        return s


def strategy(row, wallet):
    now = row[0].to_pydatetime()

    # strategy

    # if row.roll_short < row.roll_mid:
    #     # price = int(row.close * 0.99)
    #     price = int(row.close * 1.01)
    #     if wallet.btc >= (0.01 * (SATOSHI)):
    #         # print("SELL ORDER")
    #         order = Order("SELL", price, int(0.01 * SATOSHI), now)
    #         wallet.add_order(order)
    if wallet.btc >= (0.01 * (SATOSHI)):
        price = int(row.close * 1.05)
        order = Order("SELL", price, int(0.01 * SATOSHI), now)
        wallet.add_order(order)
    # elif row.roll_short > row.roll_mid:
    if row.roll_short > row.roll_mid:
        # price = int(row.close * 1.01)
        price = int(row.close * 0.99)
        if wallet.jpy > int(price * 0.01):
            # print("BUY ORDER")
            order = Order("BUY", price, int(0.01 * SATOSHI), now)
            wallet.add_order(order)


def simulate(params):
    df, index = params
    wallet = Wallet(30000, 0.00 * SATOSHI)

    exchange = Exchange()

    df_ = df[index:index+43200]
    # df_ = df[index:]

    # Loop
    for row in df_.itertuples():
        strategy(row, wallet)

        # Simulate orders
        accepted, rejected = judge_orders(
            wallet, row[0].to_pydatetime(), row.low, row.high)

        # Apply result
        wallet.cancel_orders(rejected)
        for order in accepted:
            exchange.exec_order(order, wallet)

    # finalize
    start = pd.to_datetime(df_.index[0])
    result = wallet.result(row.close)

    return (start, result)


def main():
    args = parse_args()

    # Read candle data
    df = pd.read_csv(args.input, index_col=0, parse_dates=True)

    short, mid, long = 15, 60, 720

    df['roll_short'] = df['close'].rolling(short).mean()
    df['roll_mid'] = df['close'].rolling(mid).mean()
    df['roll_long'] = df['close'].rolling(long).mean()

    print("Data size: {}".format(len(df)))

    initial_num_list = [(df, np.random.randint(0, len(df) - 43200))
                        for _ in range(args.test_iter)]

    with Pool(args.thread_size) as pool:
        imap = pool.imap(simulate, initial_num_list)
        result_list = list(tqdm(imap, total=len(initial_num_list)))
    # result_list = []
    # result_list.append(simulate((df, np.random.randint(0, len(df) - 43200))))

    starts = []
    results = []
    with open(args.output, "w") as f:
        write_data = ['{}, {}'.format(ret[0], ret[1]) for ret in result_list]
        f.write('\n'.join(write_data))
        f.write('\n')

    for result in result_list:
        starts.append(mdates.date2num(result[0]))
        results.append(result[1])

    results = np.array(results)

    print("[Result]")
    print("Average: {:5.2f}".format(np.mean(results)))
    print("Standard Deviation: {:4.2f}".format(np.std(results)))


if __name__ == '__main__':
    main()
