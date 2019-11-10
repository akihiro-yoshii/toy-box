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

def moving_average(target, move=5):
    ret_list = []
    tmp_deque = deque()
    for t in target:
        if len(tmp_deque) < move:
            tmp_deque.append(t)
            ret_list.append(sum(tmp_deque) / len(tmp_deque))
        else:
            trash = tmp_deque.popleft()
            tmp_deque.append(t)
            ret_list.append(ret_list[-1] - trash/move + t/move )

    return ret_list
