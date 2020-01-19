import argparse
import pybitflyer
from collections import deque
import pickle
import time

from bitflyer import Execution
from get_executions import separate, trace_executions


api = pybitflyer.API()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=str, help="output data")
    parser.add_argument("daily_data", type=str, help="Directory of daily data")
    parser.add_argument("--continue_from", type=str, required=True,
                        help="before data")

    return parser.parse_args()


def load_executions(path):
    with open(path, mode="rb") as f:
        executions = pickle.load(f)
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


def main():
    args = parse_args()

    # Load executions
    executions = load_executions(args.continue_from)
    print("{} contains {} data.".format(
        args.continue_from, len(executions)))

    # get data from last time
    last_id = executions[-1].id
    tmp_executions = rollback_executions(last_id)

    print("Get {} executions by rollback".format(len(tmp_executions)))
    for e in reversed(tmp_executions):
        executions.append(e)

    executions = separate(executions, args.daily_data)
    with open(args.output, mode="wb") as f:
        pickle.dump(executions, f)

    ################
    # Polling data
    ################
    last_id = executions[-1].id
    trace_executions(last_id, executions, args.output, args.daily_data)


if __name__ == '__main__':
    main()
