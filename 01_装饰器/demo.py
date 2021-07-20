# 定义一个函数
def test(number):

    # 在函数内部再定义一个函数，并且这个函数用到了外边函数的变量，那么将这个函数以及用到的一些变量称之为闭包
    def test_in(number_in):
        print("in test_in 函数, number_in is %d" % number_in)
        return number+number_in
    # 其实这里返回的就是闭包的结果
    return test_in


# 给test函数赋值，这个20就是给参数number
ret = test(20)
print(ret)

# 注意这里的100其实给参数number_in
print(ret(100))

#注 意这里的200其实给参数number_in
print(ret(200))

print("="*50)

# 引出装饰器，例子
def set_func(func):
    def call_func():
        print("=====1=====")
        print("=====2=====")
        func()
    return call_func

# @set_func
def test1():
    print("===这是test1函数====")

test1()  # 直接调用函数

ret = set_func(test1)  # ret指向函数call_func，返回值是call_func函数内的代码
print(ret)  # <function set_func.<locals>.call_func at 0x109f00400>

ret()
# 返回
# =====1=====
# =====2=====
# ===这是test函数====
print("-"*50)

# 使用装饰器
@set_func
def test2():
    print("===这是test2函数====")

test2() # 用直接调用函数的方式，等价于ret = set_func(test1) ，ret()

# 1、
# python解释器就会从上到下解释代码，步骤如下：
# def set_func(func): ==>将set_func函数加载到内存
# @set_func

# 2、
# 执行set_func函数 ，并将 @set_func 下面的函数作为set_func函数的参数，
# 即：@set_func 等价于 set_func(test2) 所以，内部就会去执行：
# def call_func():
#     print("=====1=====")
#     print("=====2=====")
#     test2()  # func是参数，此时 func 等于 test2
# return call_func # 返回 call_func，call_func代表的是函数，非执行函数 ,其实就是将原来的 test2 函数塞进另外一个函数中

# 3、
# 将执行完的set_func函数返回值 赋值 给@set_func下面的函数的函数名test2 即将set_func的返回值再重新赋值给 test2，即：
# 新test2 = def call_func():
#               print("=====1=====")
#               print("=====2=====")
#               原来的test2()
#           return call_func
