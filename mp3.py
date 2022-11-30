from multiprocessing import Process,Pipe
import numpy as np
def func2(cc):
    while True:
        a = list(range(100))
        b = list(range(10))
        d = list(range(5))
        cc.send(d)