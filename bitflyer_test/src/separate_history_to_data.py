import pybitflyer
from collections import deque
import pickle
import time
import os
import datetime

from bitflyer import Execution
import my_key as key

def get_date_start(dt):
    return datetime.datetime(
        year=dt.year, month=dt.month, day=dt.day,
        hour=4)

def main():
    filename = 'data/executions_descend.pkl'

    executions = deque()
    cnt = 0
    with open(filename, mode="rb") as f:
        while True:
            try:
                tmp = pickle.load(f)
                executions.extend(tmp)
            except EOFError:
                break

        print(len(executions))

    start = get_date_start(executions[-1].exec_date)
    delta = datetime.timedelta(days=1)
    end = start + delta

    print(start)
    while end < datetime.datetime.now():
        print(end)
        tmp_queue = deque()
        while len(executions) > 0:
            e = executions.pop()
            if e.exec_date < end:
                tmp_queue.append(e)
            else:
                executions.append(e)
                break

        if len(executions) == 0:
            executions = tmp_queue
            executions.reverse()
            break

        with open('data/executions/{:04d}{:02d}{:02d}.pkl'.format(
                start.year, start.month, start.day), mode="wb") as f:
            pickle.dump(tmp_queue, f)

        start = end
        end = end + delta

    with open('data/executions/remain.pkl', mode="wb") as f:
        pickle.dump(reversed(executions), f)


if __name__=='__main__':
    main()
