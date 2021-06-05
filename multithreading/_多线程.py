import time
import threading

def main():
    print("我在睡觉😪")
    time.sleep(1)

if __name__ == '__main__':

    for i in range(10):
        t = threading.Thread(target=main)
        t.start() # 启动线程，即让线程开始执行


'''
可以明显看出使用了多线程并发的操作，花费时间要短很多
当调用start()时，才会真正的创建线程，并且开始执行
'''