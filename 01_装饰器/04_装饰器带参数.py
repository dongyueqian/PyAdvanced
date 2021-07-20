
def info(value):
    def set_fun3(func):
        def wrapped_func(*args, **kwargs):
            print(value)
            return func(*args, **kwargs)
        return wrapped_func
    return set_fun3

# 下面的装饰过程
# 1. info("aa")
# 2. 将步骤1得到的返回值，即set_fun3返回， 然后set_fun3(foo3)
# 3. 将set_fun3(foo3)的结果返回，即wrapped_func
# 4. 让foo3 = wrapped_fun，即foo3现在指向wrapped_func

@info("aa")
def foo3():
    print("I am foo----3")

@info("bb")
def foo4():
    print("I am foo----4")

foo3() # foo3()==info("aa")(foo3)()
foo4()
"""
运行结果：
aa
I am foo----3
bb
I am foo----4
"""

print("="*80)