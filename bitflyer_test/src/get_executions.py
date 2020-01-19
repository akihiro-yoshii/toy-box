import argparse
import pybitflyer
from collections import deque
import pickle
import time
import datetime
import os

from bitflyer import Execution


api = pybitflyer.API()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=str, help="output data")
    parser.add_argument("daily_data", type=str, help="Directory of daily data")

    return parser.parse_args()


def get_date_start(dt):
    return datetime.datetime(
        year=dt.year, month=dt.month, day=dt.day,
        hour=4)


def separate(executions, daily_data_path):
    start = get_date_start(executions[0].exec_date)
    delta = datetime.timedelta(days=1)
    end = start + delta

    while end < datetime.datetime.now():
        tmp_queue = deque()
        while len(executions) > 0:
            e = executions.popleft()
            if e.exec_date < end:
                tmp_queue.append(e)
            else:
                executions.appendleft(e)
                break

        if len(executions) > 0:
            path = os.path.join(daily_data_path,
                                "{:04d}{:02d}{:02d}.pkl".format(
                                    start.year, start.month, start.day))
            with open(path, mode="wb") as f:
                pickle.dump(tmp_queue, f)
        else:
            tmp_queue.extend(executions)
            executions = tmp_queue
            break

        start = end
        end = end + delta

    return executions


def rollback_executions(last_id):
    raw_executions = api.executions(after=last_id, count=500)

    executions = deque()
    while True:
        for r in raw_executions:
            e = Execution(r)
            if e.id <= last_id:
                break
            executions.append(e)

        if len(raw_executions) < 500:
            break

        print("RollBacking...")
        first_id = executions[-1].id

        time.sleep(3)
        raw_executions = api.executions(
            after=last_id, before=first_id, count=500)

    return executions


def trace_executions(last_id, executions, output, daily_data_path):
    while True:
        print(executions[-1].exec_date)
        time.sleep(60)
        ret = api.executions(after=last_id, count=500)
        for r in reversed(ret):
            e = Execution(r)
            executions.append(e)

        executions = separate(executions, daily_data_path)
        with open(output, mode="wb") as f:
            pickle.dump(executions, f)

        last_id = executions[-1].id


def main():
    args = parse_args()

    executions = deque()

    # 1st calling
    raw_executions = api.executions(count=500)
    for r in reversed(raw_executions):
        e = Execution(r)
        executions.append(e)

    executions = separate(executions, args.daily_data)
    with open(args.output, mode="wb") as f:
        pickle.dump(executions, f)

    # Polling data
    last_id = executions[-1].id
    trace_executions(last_id, executions, args.output, args.daily_data)


if __name__ == '__main__':
    main()
