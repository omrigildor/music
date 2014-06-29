import time
import os
import thread
os.chdir(os.path.abspath("/Users/omrigildor/PingPong"))

def thread1(t, word):
    while 1:
        for x in os.listdir(os.getcwd()):
            if x.endswith("ping"):
                os.rename(x, x[:2] + "pong")
                print word
                time.sleep(t)


def thread2(t, word):
    while 1:
        for x in os.listdir(os.getcwd()):
            if x.endswith("pong"):
                os.rename(x, x[:2] + "ping")
                print word
                time.sleep(t)

thread.start_new(thread1, (4, "ping"))
thread.start_new(thread2, (1, "hi"))

while 1:
    pass