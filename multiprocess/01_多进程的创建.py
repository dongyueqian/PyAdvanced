from multiprocessing import Process
import time

'''
multiprocessing模块就是跨平台版本的多进程模块，提供了一个Process类
来代表一个进程对象，这个对象可以理解为是一个独立的进程，可以执行另外的事情
'''

def test(arg):
    # 子进程要执行的代码
    while True:
        print("------子进程-------：%s" % arg)
        time.sleep(1)

if __name__ == '__main__':
    # 创建一个Process对象然后调用它的start()方法来生成进程
    p = Process(target = test, args = ("哈哈哈哈哈",))
    p.start()
    while True:
        print("------主进程------")
        time.sleep(1)

# 创建子进程时，只需要传入一个执行函数和函数的参数，创建一个Process实例，用start()方法启动