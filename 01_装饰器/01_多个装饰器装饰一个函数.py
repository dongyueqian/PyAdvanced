def set_func(func):
    print("开始装饰------1")
    def call_func():
        print("设置.......")
        func()
    return call_func

def get_func(func):
    print("开始装饰------2")
    def call_func():
        print("获取.......")
        func()
    return call_func

# @set_func
# @get_func
# def demo1():
#     print("测试....")

# demo1()
"""
运行结果：
开始装饰------2
开始装饰------1
设置.......
获取.......
测试....
"""

def set_mark1(func):
    print("开始装饰------3")
    def call_func():
        return "<h1>" + func()+ "</h1>"
    return call_func

def set_mark2(func):
    print("开始装饰------4")
    def call_func():
        return "<t1>"+func()+"</t1>"
    return call_func

@set_mark1
@set_mark2
def demo2():
    return "测试...."

print(demo2())
"""
运行结果：
开始装饰------4
开始装饰------3
<h1><t1>测试....</t1></h1>
"""
