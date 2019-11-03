import pybitflyer
from collections import deque
import pickle
import time
import os

from bitflyer import Execution
import my_key as key

def main():
    api = pybitflyer.API(api_key=key.bitflyer['key'], api_secret=key.bitflyer['secret'])

    filename = 'test.pkl'

    with open(filename, mode="wb") as f:
        pass

    ret = api.executions(count=500)

    print(ret[0]['exec_date'])

    while True:
        executions = deque()
        for r in ret:
            executions.append(Execution(r))

        with open(filename, mode="ab") as f:
            pickle.dump(executions, f)

        print(executions[-1].exec_date)

        first_id = executions[-1].id

        time.sleep(3)
        ret = api.executions(before=first_id, count=500)


if __name__=='__main__':
    main()
