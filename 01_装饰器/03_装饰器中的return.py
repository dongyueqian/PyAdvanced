from time import ctime, sleep

def timefun(func):
    def wrapped_func():
        print("%s called at %s" % (func.__name__, ctime()))
        func()
        # return func() # 一般情况下为了让装饰器更通用，可以有return
                        # return func() 即可返回getInfo函数内的内容
    return wrapped_func

@timefun
def foo():
    print("I am foo")

@timefun
def getInfo():
    return '----hahah---'

foo()
sleep(0.5)
foo()
print(getInfo())  # None,之所以为None，是因为第5行没有返回值，改成
                  # return func()即可返回getInfo函数内的内容


"""
运行结果：
foo called at Sat Jul 17 12:27:52 2021
I am foo
foo called at Sat Jul 17 12:27:52 2021
I am foo
getInfo called at Sat Jul 17 12:27:52 2021
None
"""


