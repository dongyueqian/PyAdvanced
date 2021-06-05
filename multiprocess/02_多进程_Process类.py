from multiprocessing import Process
import os

def main(arg):
    info("main ")
    print(arg)

def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())

if __name__ == '__main__':
    # 创建一个Process对象然后调用它的start()方法来生成进程
    p = Process(target=main, args=('xixiix',))
    p.start()
    p.join()