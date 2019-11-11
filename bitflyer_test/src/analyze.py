from collections import deque

class TimeData(object):
    def __init__(self, **kwargs):
        self.open = kwargs['open']
        self.close = kwargs['close']
        self.low = kwargs['low']
        self.high = kwargs['high']
        self.volume = kwargs['volume']
        self.start = kwargs['start']
        self.end = kwargs['end']

    def __str__(self):
        s = "[{:}] open: {:7.0f}, close: {:7.0f}, volume:{:12.8f}"
        s = s.format(self.start, self.open, self.close, self.volume)
        return s
