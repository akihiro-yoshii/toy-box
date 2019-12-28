import argparse
import pandas as pd
import datetime
from collections import deque


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=str, help="path of candle csv")

    return parser.parse_args()


class Exchange(object):
    def __init__(self):
        self.orders = deque()

    def add_order(self, order, wallet):
        # TODO: 財布からお金を引き出しておく
        self.orders.append(order)

    def judge_orders(self, current):
        remain = deque()
        executed = deque()

        now = current[0].to_pydatetime()

        while len(self.orders) > 0:
            order = self.orders.popleft()

            if now >= order.begin:
                if judge_order(current, order):
                    executed.append(order)
                else:
                    remain.append(order)
            else:
                remain.append(order)

        self.orders = remain

        return executed

    def __repr__(self):
        s = "[Order]\n"
        s += "side: {}\n".format(self.side)
        s += "price: {}\n".format(self.price)
        s += "size: {}\n".format(self.size)
        s += "begin: {}\n".format(self.begin)
        return s


class Wallet(object):
    def __init__(self, jpy, btc):
        self.jpy = jpy
        self.btc = btc

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
        s += "btc: {}\n".format(self.btc)
        return s


class Order(object):
    def __init__(self, side, price, size, begin):
        self.side = side
        self.price = price
        self.size = size
        self.begin = begin + datetime.timedelta(minutes=1)

    def __repr__(self):
        s = "[Order]\n"
        s += "side: {}\n".format(self.side)
        s += "price: {}\n".format(self.price)
        s += "size: {}\n".format(self.size / (10**8))
        s += "begin: {}\n".format(self.begin)
        return s


def judge_order(candle, order):
    ret = None
    if order.side == "BUY":
        ret = True if order.price > candle.low else False
    elif order.side == "SELL":
        ret = True if order.price < candle.high else False
    return ret

def main():
    args = parse_args()

    wallet = Wallet(30000, 0)
    print(wallet)

    # Read candle data
    df = pd.read_csv(args.input, index_col=0, parse_dates=True)

    exchange = Exchange()

    # Test Order
    order = Order("BUY", 800000, int(0.01 * (10**8)), datetime.datetime(2019, 11, 16, 12, 30, 0))
    exchange.add_order(order, None)
    exchange.add_order(order, None)
    # print(test_order)
    # Loop


    for row in df.itertuples():
        # Dicide order or not

        # Simulate orders
        ret = exchange.judge_orders(row)

        # Apply result
        if len(ret) > 0:
            print(row)
        for order in ret:
            # order = ret[0]
            print(order)
            wallet.gain("JPY", order.price * order.size // (10**8))
            order = None

    print(wallet)




if __name__ == '__main__':
    main()
