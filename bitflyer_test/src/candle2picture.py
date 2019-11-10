import csv
import datetime

from analyze import *

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import mpl_finance as mpf

import matplotlib.dates as mdates


def main():
    # read
    quotes = []
    starts = []
    closes = []
    with open('test.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            tmp = []
            tmp.append(mdates.date2num(datetime.datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S')))
            tmp.extend([float(v) for v in row[1:-1]])
            quotes.append(tmp)
            starts.append(tmp[0])
            closes.append(float(tmp[2]))


    # calc move avarage
    move_5 = moving_average(closes, move=5)
    move_15 = moving_average(closes, move=15)
    move_60 = moving_average(closes, move=60)
    move_240 = moving_average(closes, move=240)

    # Plot Figure
    fig = plt.figure()
    ax = plt.subplot()

    mpf.candlestick_ochl(ax, quotes, width=0.001, colorup='g', colordown='r', alpha=0.75)

    ax.plot(starts, move_5)
    ax.plot(starts, move_15)
    ax.plot(starts, move_60)
    ax.plot(starts, move_240)

    ax.grid() #グリッド表示

    locator = mdates.AutoDateLocator()
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(mdates.AutoDateFormatter(locator))
    fig.autofmt_xdate() #x軸のオートフォーマット

    fig.savefig("test.png")



if __name__ == '__main__':
    main()
