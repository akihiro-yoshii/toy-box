import argparse
import pandas as pd
import datetime
from collections import deque
import numpy as np
from tqdm import trange

import matplotlib
import matplotlib.dates as mdates
matplotlib.use('Agg')
import matplotlib.pyplot as plt  # NOQA

SATOSHI = 10 ** 8


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=str, help="path of candle csv")

    return parser.parse_args()


class Exchange(object):
    def exec_order(self, order, wallet):
        if order.side == "SELL":
            wallet.gain("JPY", order.price * order.size // (SATOSHI))
        elif order.side == "BUY":
            wallet.gain("BTC", order.size)
        # TODO: ValueError other type

    def cancel_all_orders(self, wallet):
        while len(walllet.orders):
            order = wallet.orders.popleft()
            if order.side == "SELL":
                wallet.gain("BTC", order.size)
            elif order.side == "BUY":
                wallet.gain("JPY", order.price * order.size // (SATOSHI))
            # TODO: ValueError other type


    def judge_orders(self, current, wallet):
        remain = deque()
        accepted = deque()
        rejected = deque()

        now = current[0].to_pydatetime()

        while len(wallet.orders) > 0:
            order = wallet.orders.popleft()

            if now >= order.end:
                rejected.append(order)
            elif now >= order.begin:
                if judge_order(current, order):
                    accepted.append(order)
                else:
                    remain.append(order)
            else:
                remain.append(order)

        wallet.orders = remain

        return accepted, rejected

    def __repr__(self):
        s = "[Order]\n"
        s += "side: {}\n".format(self.side)
        s += "price: {}\n".format(self.price)
        s += "size: {}\n".format(self.size)
        s += "begin: {}\n".format(self.begin)
        return s


def judge_order(candle, order):
    ret = None
    if order.side == "BUY":
        ret = True if order.price > candle.low else False
    elif order.side == "SELL":
        ret = True if order.price < candle.high else False
    # TODO: ValueError other type
    return ret


class Wallet(object):
    def __init__(self, jpy, btc):
        self.jpy = jpy
        self.btc = btc

        self.orders = deque()

    def add_order(self, order):
        if order.side == "BUY":
            self.pay("JPY", order.price * order.size // (SATOSHI))
        elif order.side == "SELL":
            self.pay("BTC", order.size)
        # TODO: ValueError other type

        self.orders.append(order)

    def cancel_orders(self, orders):
        while len(orders):
            order = orders.popleft()
            if order.side == "SELL":
                self.gain("BTC", order.size)
            elif order.side == "BUY":
                self.gain("JPY", order.price * order.size // (SATOSHI))
            # TODO: ValueError other type

    def pay(self, type, size):
        if type == "JPY":
            # TODO: 整数チェック
            self.jpy -= size
        elif type == "BTC":
            self.btc -= size
        # TODO: ValueError other type

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
            if order.side == "SELL":
                tmp_btc += order.size
            else:
                tmp_jpy += order.price * order.size // SATOSHI

        total = int((self.jpy + tmp_jpy) + (self.btc + tmp_btc) * close // SATOSHI)
        return total


class Order(object):
    def __init__(self, side, price, size, begin):
        self.side = side
        self.price = price
        self.size = size
        self.begin = begin + datetime.timedelta(minutes=1)
        self.end = begin + datetime.timedelta(days=7)

    def __repr__(self):
        s = "[Order]\n"
        s += "side: {}\n".format(self.side)
        s += "price: {}\n".format(self.price)
        s += "size: {}\n".format(self.size / SATOSHI)
        s += "begin: {}\n".format(self.begin)
        return s


def main():
    args = parse_args()

    # Read candle data
    df = pd.read_csv(args.input, index_col=0, parse_dates=True)

    short, mid, long = 60, 120, 720

    df['roll_short'] = df['close'].rolling(short).mean()
    df['roll_mid'] = df['close'].rolling(mid).mean()
    df['roll_long'] = df['close'].rolling(long).mean()

    print(len(df))

    starts = []
    results = []

    for _ in trange(1000):
    # for _ in trange(20):

        wallet = Wallet(30000, 0.00 * SATOSHI)

        exchange = Exchange()

        index = np.random.randint(0, len(df) - 43200)
        df_ = df[index:index+43200]
        # df_ = df[index:]

        # Loop
        for row in df_.itertuples():
            now = row[0].to_pydatetime()

            # Dicide order or not

            # strategy
            if row.roll_short < row.roll_mid:
                # price = int(row.close * 0.99)
                price = int(row.close * 1.01)
                if wallet.btc >= (0.01 * (SATOSHI)):
                    # print("SELL ORDER")
                    order = Order("SELL", price, int(0.01 * SATOSHI), now)
                    wallet.add_order(order)
            # elif row.roll_mid > row.roll_long:
            elif row.roll_short > row.roll_mid:
                # price = int(row.close * 1.01)
                price = int(row.close * 0.99)
                if wallet.jpy > int(price * 0.01):
                    # print("BUY ORDER")
                    order = Order("BUY", price, int(0.01 * SATOSHI), now)
                    wallet.add_order(order)

            # Simulate orders
            ret, rejected = exchange.judge_orders(row, wallet)

            # Apply result
            wallet.cancel_orders(rejected)
            for order in ret:
                # print(order.side)
                exchange.exec_order(order, wallet)

        # finalize
        start = mdates.date2num(pd.to_datetime(df_.index[0]))
        starts.append(start)
        results.append(wallet.result(row.close))

    # print(exchange.orders)
    results = np.array(results)
    print(np.mean(results))
    print(np.std(results))

    # fig = plt.figure(figsize=(16.0, 9.0))
    # plt.hist(results, bins=50)
    # plt.savefig("test.png")
    # plt.cla()
    fig, ax = plt.subplots(figsize=(16, 9))
    ax.scatter(starts, results)
    locator = mdates.AutoDateLocator()
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%y/%m/%d %H:%M'))
    fig.savefig("result.png")


if __name__ == '__main__':
    main()
