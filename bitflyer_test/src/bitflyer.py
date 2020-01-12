import datetime


class Execution(object):
    def __init__(self, d=None):
        if d is not None:
            self.id = int(d['id'])
            self.side = d['side']
            self.price = int(d['price'])
            self.size = round(float(d['size']) * (10**8))
            self.exec_date = timestamp_to_datetime(d['exec_date'])
            self.buy_child_order_acceptance_id = \
                d['buy_child_order_acceptance_id']
            self.sell_child_order_acceptance_id = \
                d['sell_child_order_acceptance_id']
        else:
            pass

    def __repr__(self):
        s = "[Execution]\n"
        s += "id: {}\n".format(self.id)
        s += "side: {}\n".format(self.side)
        s += "price: {}\n".format(self.price)
        s += "size: {}\n".format(self.size)
        s += "exec_date: {}\n".format(self.exec_date)
        return s


def timestamp_to_datetime(ts):
    if len(ts) == 21:
        ts += '0'
    if len(ts) == 22:
        ts += '0'
    return datetime.datetime.fromisoformat(ts)
