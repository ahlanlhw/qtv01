from multiprocessing import Process,Pipe
import numpy as np
def func1(c):
    while True:
        a = list(range(100))
        b = list(range(10))
        c.send(b)