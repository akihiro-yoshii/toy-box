from collections import deque
import pickle
import datetime

from bitflyer import Execution


def open_executions(path):
    with open(path, mode="rb") as f:
        executions = pickle.load(f)
    return executions


def get_minute(dt):
    return datetime.datetime(
        year=dt.year,
        month=dt.month,
        day=dt.day,
        hour=dt.hour,
        minute=dt.minute)


def pickup_term(executions, start, end):
    target = deque()
    for e in executions:
        tmp_dt = e.exec_date
        if start < tmp_dt < end:
            target.append(e)
        else:
            continue

    return target


def summary_executions(executions):
    open_price = executions[0].price
    close = executions[-1].price
    low = min(executions, key=lambda e: e.price).price
    high = max(executions, key=lambda e: e.price).price
    total_size = 0.0
    for e in executions:
        total_size += e.size

    return open_price, close, low, high, total_size


def main():
    # Open pkl
    executions = deque()
    files = ['data/executions/20191003.pkl', 'data/executions/20191004.pkl']
    for f in files:
        executions.extend(open_executions(f))

    # pickup from list
    ## 何もない期間どうするか？
    start = get_minute(executions[0].exec_date)
    end = start + datetime.timedelta(minutes=1)
    target = pickup_term(executions, start, end)

    # Get low/high/open/close/volume
    print(summary_executions(target))

    # Save Info

if __name__=='__main__':
    main()
