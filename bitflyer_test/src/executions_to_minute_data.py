from collections import deque
import pickle
import datetime

import timer_functions

from analyze import TimeData

import csv
import glob


def open_executions(path):
    with open(path, mode="rb") as f:
        executions = pickle.load(f)
    return executions


# def pickup_term(executions, start, end):
def pickup_term(executions, end):
    target = deque()
    # for e in executions:
    #     tmp_dt = e.exec_date
    #     if start < tmp_dt < end:
    #         target.append(e)
    #     else:
    #         continue
    while len(executions) > 0:
        if executions[0].exec_date < end:
            target.append(executions.popleft())
        else:
            break

    return target


def summary_executions(executions):
    open_price = executions[0].price
    close = executions[-1].price
    low = min(executions, key=lambda e: e.price).price
    high = max(executions, key=lambda e: e.price).price
    volume = 0.0
    for e in executions:
        volume += e.size

    return open_price, close, low, high, volume


def main():
    # Open pkl
    executions = deque()
    files = glob.glob('data/executions/*')
    for f in files:
        executions.extend(open_executions(f))

    # Sort executions
    executions = list(executions)
    executions.sort(key=lambda e: e.exec_date)
    executions = deque(executions)

    # Loop
    span = 60  # minutes
    start = timer_functions.mask_time(executions[0].exec_date, mask="seconds")
    end = start + datetime.timedelta(minutes=span)

    # pickup from list
    tds = []
    while end < timer_functions.mask_time(
            executions[-1].exec_date) + datetime.timedelta(minutes=1):
        # target = pickup_term(executions, start, end)
        target = pickup_term(executions, end)

        if len(target) > 0:
            # Get open/close/low/high/volume
            open_price, close, low, high, volume = summary_executions(target)
        else:
            open_price = close
            low = close
            high = close
            volume = 0.0

        td = TimeData(open=open_price, close=close, low=low, high=high,
                      start=start, end=end, volume=volume)
        print(td)

        tds.append(td)

        start = end
        end = start + datetime.timedelta(minutes=span)

    # Save Info
    with open('test.csv', 'w') as f:
        writer = csv.writer(f)
        for td in tds:
            writer.writerow([td.start, td.open, td.close,
                             td.high, td.low, td.volume])


if __name__ == '__main__':
    main()
