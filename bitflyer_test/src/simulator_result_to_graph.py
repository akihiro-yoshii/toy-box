import argparse
import numpy as np
from datetime import datetime as dt

import matplotlib
import matplotlib.dates as mdates
matplotlib.use('Agg')
import matplotlib.pyplot as plt  # NOQA


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=str, help="path of candle csv")
    parser.add_argument("output", type=str, help="path of result graph")

    # optional argument
    return parser.parse_args()


def main():
    args = parse_args()

    starts = []
    results = []
    with open(args.input) as f:
        for line in f:
            line = line.split(', ')
            start = dt.strptime(line[0], "%Y-%m-%d %H:%M:%S")
            starts.append(mdates.date2num(start))
            results.append(int(line[1]))

    results = np.array(results)

    # output
    fig, ax = plt.subplots(figsize=(16, 9))
    ax.scatter(starts, results, s=5)
    locator = mdates.AutoDateLocator()
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%y/%m/%d %H:%M'))
    fig.savefig(args.output)


if __name__ == '__main__':
    main()
