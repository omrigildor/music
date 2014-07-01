import time
import os
import thread
from Queue import Queue
import signal

os.chdir(os.path.abspath("/Users/omrigildor/PingPong"))

def thread1(t, q):
    count = 0
    while 1:
        for x in os.listdir(os.getcwd()):
            if x.endswith("ping"):
                os.rename(x, x[:2] + "pong")
                count += 1

        q.put(("t1", count))
        count = 0
        time.sleep(t)


def thread2(t, q):
    count = 0
    while 1:
        for x in os.listdir(os.getcwd()):
            if x.endswith("pong"):
                os.rename(x, x[:2] + "ping")
                count += 1

        q.put(("t2", count))
        count = 0
        time.sleep(t)




q = Queue()
thread.start_new(thread1, (1,q))
thread.start_new(thread2, (2,q))


while 1:
    pass