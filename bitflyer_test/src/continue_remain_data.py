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

def separate(executions):
    start = get_date_start(executions[0].exec_date)
    delta = datetime.timedelta(days=1)
    end = start + delta

    while end < datetime.datetime.now():
        print(end)
        tmp_queue = deque()
        while len(executions) > 0:
            e = executions.popleft()
            if e.exec_date < end:
                tmp_queue.append(e)
            else:
                executions.appendleft(e)
                break

        if len(executions) > 0:
            with open('data/executions/{:04d}{:02d}{:02d}.pkl'.format(
                    start.year, start.month, start.day), mode="wb") as f:
                pickle.dump(tmp_queue, f)
        else:
            # executions = tmp_queue.extend(executions)
            tmp_queue.extend(executions)
            executions = tmp_queue
            break

        start = end
        end = end + delta

    return executions


def main():
    ########
    # Load
    ########
    filename = 'data/executions/remain.pkl'

    executions = deque()
    with open(filename, mode="rb") as f:
        tmp = pickle.load(f)
        executions.extend(tmp)

    # last_id = 0
    # for e in executions:
    #     print(e.id - last_id)
    #     last_id = e.id

    print(len(executions))
    print(executions[-1].exec_date)

    ########
    # RollBack
    ########
    last_id = executions[-1].id

    api = pybitflyer.API(api_key=key.bitflyer['key'], api_secret=key.bitflyer['secret'])

    ret = api.executions(after=last_id, count=500)

    tmp_queue = deque()
    while True:
        for r in ret:
            e = Execution(r)
            if e.id <= last_id:
                break
            tmp_queue.append(e)

        if len(ret) < 500:
            break

        print("RollBacking...")
        first_id = tmp_queue[-1].id

        time.sleep(3)
        ret = api.executions(after=last_id, before=first_id, count=500)

    print(len(tmp_queue))
    for e in reversed(tmp_queue):
        executions.append(e)

    print(len(executions))
    print(executions[-1].exec_date)

    executions = separate(executions)
    with open('data/executions/remain.pkl', mode="wb") as f:
        pickle.dump(executions, f)


    ########
    # kanshi
    ########
    last_id = executions[-1].id
    while True:
        time.sleep(60)
        ret = api.executions(after=last_id, count=500)
        for r in reversed(ret):
            e = Execution(r)
            executions.append(e)

        executions = separate(executions)
        with open('data/executions/remain.pkl', mode="wb") as f:
            pickle.dump(executions, f)

        last_id = executions[-1].id

        print(executions[-1].exec_date)



if __name__=='__main__':
    main()
