import pybitflyer
import datetime
from collections import deque

import time

import my_key as key

class Execution(object):
    def __init__(self, d):
        self.id = int(d['id'])
        self.side = d['side']
        self.price = float(d['price'])
        self.size = float(d['size'])
        self.exec_date = timestamp_to_datetime(d['exec_date'])
        self.buy_child_order_acceptance_id = d['buy_child_order_acceptance_id']
        self.sell_child_order_acceptance_id = d['sell_child_order_acceptance_id']

    def __repr__(self):
        s = "[Execution]\n"
        s += "id: {}\n".format(self.id)
        s += "side: {}\n".format(self.side)
        s += "price: {}\n".format(self.price)
        s += "size: {}\n".format(self.size)
        s += "exec_date: {}\n".format(self.exec_date)
        return s

def timestamp_to_datetime(ts):
    if len(ts) == 21:
        ts += '0'
    if len(ts) == 22:
        ts += '0'
    return datetime.datetime.fromisoformat(ts)

def get_minute(dt):
    return datetime.datetime(
        year=dt.year,
        month=dt.month,
        day=dt.day,
        hour=dt.hour,
        minute=dt.minute)

def average(executions):
    total_size = 0.0
    total_value = 0.0
    for e in executions:
        total_size += e.size
        total_value += e.size * e.price

    return total_value / total_size

def main():
    api = pybitflyer.API(api_key=key.bitflyer['key'], api_secret=key.bitflyer['secret'])

    # ret = api.board(product_code='BTC_JPY')
    # print(ret['mid_price'])

    ret = api.executions(count=1000)
    executions = deque()
    for r in reversed(ret):
        executions.append(Execution(r))

    # for e in executions:
    #     print(e)

    executions, last_id = printMinuteAverage(executions)

    while True:
        time.sleep(120)
        print("Call API")
        ret = api.executions(after=last_id)
        for r in reversed(ret):
            executions.append(Execution(r))

        executions, last_id = printMinuteAverage(executions)


def printMinuteAverage(executions):
    start = get_minute(executions[0].exec_date)
    delta = datetime.timedelta(minutes=1)
    end = start + delta

    last_id = executions[-1].id

    while True:
        target = []
        while len(executions) > 0:
            e = executions.popleft()
            tmp_dt = e.exec_date
            if tmp_dt < end:
                target.append(e)
            else:
                executions.appendleft(e)
                break

        if len(executions) == 0:  # まだ1分経過していない場合
            target = deque(target)
            return target, last_id # TODO
        elif len(target) == 0:  # 1分に何も取引されていない場合
            print("[{}] {:.2f}".format(start, ave))
        else:  # 他ケースではもう一回処理を行いたい
            ave = average(target)
            print("[{}] {:.2f}".format(start, ave))

        start = end
        end = end + delta


if __name__=='__main__':
    main()
