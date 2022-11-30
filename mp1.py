from multiprocessing import Process,Queue,Pipe
from mp2 import func1
from mp3 import func2

if __name__ == '__main__':
    p,c=Pipe()
    q,cc = Pipe()
    pp = Process(target=func1,args=(c,))
    qq = Process(target=func2,args=(cc,))
    pp.start()
    qq.start()
    while True:
        b = p.recv()
        d = q.recv()
        print(b,'\n\n',d)