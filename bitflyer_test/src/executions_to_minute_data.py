from collections import deque
import pickle
import datetime
import argparse
import pandas as pd
import glob

import timer_functions


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=str, help="path of candle csv")

    parser.add_argument("--span", type=int, default=1,
                        help="Squash minutes, default=1")
    return parser.parse_args()


def open_executions(path):
    with open(path, mode="rb") as f:
        executions = pickle.load(f)
    return executions


def pickup_term(executions, end):
    target = deque()
    while len(executions) > 0:
        if executions[0].exec_date < end:
            target.append(executions.popleft())
        else:
            break

    return target


def summary_executions(executions):
    open = executions[0].price
    close = executions[-1].price
    high = max(executions, key=lambda e: e.price).price
    low = min(executions, key=lambda e: e.price).price
    volume = 0.0
    for e in executions:
        volume += e.size

    return open, close, high, low, volume


def main():
    args = parse_args()

    # Open pkl
    executions = deque()
    files = glob.glob('data/executions/*')
    for f in files:
        executions.extend(open_executions(f))
    print("LOAD EXECUTIONS")

    # Sort executions
    executions = list(executions)
    executions.sort(key=lambda e: e.exec_date)
    executions = deque(executions)

    print("SORT EXECUTIONS")

    # Loop
    start = timer_functions.mask_time(executions[0].exec_date, mask="seconds")
    span = datetime.timedelta(minutes=args.span)
    end = start + span

    # pickup from list
    starts = []
    opens = []
    closes = []
    highs = []
    lows = []
    volumes = []
    while len(executions) > 0:
        if (timer_functions.mask_time(
                executions[-1].exec_date) + span) < start:
            print("???")
            break
        target = pickup_term(executions, end)

        # Get open/close/high/low/volume
        if len(target) > 0:
            open, close, high, low, volume = summary_executions(target)
        else:
            open = high = low = close
            volume = 0.0

        starts.append(start)
        opens.append(open)
        closes.append(close)
        highs.append(high)
        lows.append(low)
        volumes.append(volume)

        start = end
        end = start + span

    df = pd.DataFrame(
        index=starts,
        columns=["open", "close", "high", "low", "volume"],
        data={"open": opens, "close": closes,
              "high": highs, "low": lows, "volume": volumes}
    )

    # Save Info
    df.to_csv(args.output)


if __name__ == '__main__':
    main()
