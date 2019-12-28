import pandas as pd
import mpl_finance as mpf
import argparse

import matplotlib
import matplotlib.dates as mdates
matplotlib.use('Agg')
import matplotlib.pyplot as plt  # NOQA


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=str, help="path of candle csv")
    parser.add_argument("output", type=str, help="path of graph")

    parser.add_argument("--output_length", type=int, default=100,
                        help="length of candle data output. If 0, print all.")
    parser.add_argument("--roll_spans", type=int, nargs="+",
                        default=[5, 15, 60], help="Plot rolling means")
    parser.add_argument("--plot_candle", action="store_true")
    return parser.parse_args()


def main():
    args = parse_args()

    # read
    df = pd.read_csv(args.input, index_col=0, parse_dates=True)
    df.index = pd.to_datetime(df.index)
    df.index = mdates.date2num(df.index)

    # rolling_average
    for span in args.roll_spans:
        name = 'roll_{}'.format(span)
        df[name] = df['close'].rolling(span).mean()

    if args.output_length > 0:
        df = df.tail(args.output_length)

    # Plot Figure
    # fig = plt.figure(figsize=(16.0, 9.0))
    fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(16, 9), sharex=True,
                             gridspec_kw={'height_ratios': [4, 1]})
    # ax = plt.subplot()

    # Plot candle
    width = (df.index[1] - df.index[0]) * 0.7
    if args.plot_candle:
        ohlc = df.reset_index().values
        width = (ohlc[1][0] - ohlc[0][0]) * 0.7
        mpf.candlestick_ochl(axes[0], ohlc, colorup='g', colordown='r',
                             width=width, alpha=0.75)
    else:
        axes[0].plot(df.index, df.close, color="black", linewidth=0.7)

    # Plot rolling means
    for span in args.roll_spans:
        name = "roll_{}".format(span)
        axes[0].plot(df.index, getattr(df, name), linewidth=0.7, label=name)

    axes[1].bar(df.index, df.volume, width=width)

    axes[0].grid(linestyle=':')
    axes[0].legend()
    axes[1].grid(linestyle=':')

    locator = mdates.AutoDateLocator()
    axes[0].xaxis.set_major_locator(locator)
    axes[0].xaxis.set_major_formatter(mdates.DateFormatter('%y/%m/%d %H:%M'))

    fig.savefig(args.output)


if __name__ == '__main__':
    main()
