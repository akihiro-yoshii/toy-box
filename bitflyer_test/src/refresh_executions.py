import glob
import pickle
from collections import deque

from bitflyer import Execution


def main():
    files = glob.glob('data/executions/*')
    files.sort()
    for path in files:
        print(path)
        with open(path, mode="rb") as f:
            old = pickle.load(f)
        print(old[0])

        new = deque()
        for old_e in old:
            e = Execution()
            e.id = old_e.id
            e.side = old_e.side
            e.price = int(old_e.price)
            e.size = round(old_e.size * (10**8))
            e.exec_date = old_e.exec_date
            e.buy_child_order_acceptance_id = old_e.buy_child_order_acceptance_id
            e.sell_child_order_acceptance_id = old_e.sell_child_order_acceptance_id
            new.append(e)
        print(new[0])

        path = path.replace('executions', 'executions_new')
        print(path)
        with open(path, mode="wb") as f:
            pickle.dump(new, f)


if __name__ == '__main__':
    main()
