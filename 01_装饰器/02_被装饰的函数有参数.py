
"""
1、被装饰的是无参数的函数
"""
def set_fun1(func):
    def wrapped_func(*args, **kwargs):
        print("哈哈哈哈-----1")
        return func(*args, **kwargs)
    return wrapped_func

# 相当于foo = timefun(foo)
# foo先做为参数赋值给func后，foo指向timefun返回的wrapped_func
@set_fun1
def foo1():
    print("I am foo----1")

# foo()：调用foo(),即等价调用wrapped_func()
# 内部函数wrapped_func被引用，所以外部函数的func变量(自由变量)并没有释放
# func里保存的是原foo函数对象
foo1()

"""
运行结果：
哈哈哈哈-----1
I am foo----1
"""

print("="*80)

"""
2、被装饰的是有参数的函数
"""
def set_fun2(func):
    def wrapped_func(*args, **kwargs):
        print("哈哈哈哈-----2")
        return func(*args, **kwargs)
    return wrapped_func

@set_fun2
def foo2(a,*args, **kwargs):
    print("I am foo----2",a)
    print("I am foo----2",a ,args)
    print("I am foo----2", a, args, kwargs)

foo2(10,20,30, m = 100)
"""
运行结果：
哈哈哈哈-----2
I am foo----2 10
I am foo----2 10 (20, 30)
I am foo----2 10 (20, 30) {'m': 100}
"""

print("="*80)