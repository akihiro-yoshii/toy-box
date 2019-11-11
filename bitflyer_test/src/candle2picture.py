import pandas as pd
import mpl_finance as mpf

import matplotlib
import matplotlib.dates as mdates
matplotlib.use('Agg')
import matplotlib.pyplot as plt  # NOQA


def main():
    # read
    column_names = ('time', 'open', 'close', 'high', 'low')
    df = pd.read_csv('test.csv', names=column_names, index_col=0,
                     parse_dates=True)

    # rolling_average
    df['roll_5'] = df['close'].rolling(5).mean()
    df['roll_25'] = df['close'].rolling(25).mean()
    df['roll_75'] = df['close'].rolling(75).mean()

    df_ = df.copy()
    df_.index = mdates.date2num(df_.index)
    ohlc = df_.tail(100).reset_index().values

    # Plot Figure
    fig = plt.figure()
    ax = plt.subplot()

    mpf.candlestick_ochl(ax, ohlc, colorup='g', colordown='r',
                         width=0.03, alpha=0.75)

    ax.plot(ohlc[:, 0], ohlc[:, 6])
    ax.plot(ohlc[:, 0], ohlc[:, 7])
    ax.plot(ohlc[:, 0], ohlc[:, 8])

    ax.grid()

    locator = mdates.AutoDateLocator()
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(mdates.AutoDateFormatter(locator))
    fig.autofmt_xdate()  # format x pole

    fig.savefig("test.png")


if __name__ == '__main__':
    main()
