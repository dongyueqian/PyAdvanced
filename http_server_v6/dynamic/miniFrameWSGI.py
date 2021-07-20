import re

# 把path和对应的函数放在字典里
url_func_dict = dict()

# 装饰器
def route(url_path):
    def set_fun(func):
        url_func_dict[url_path] = func
        def wrapped_func(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapped_func
    return set_fun

@route("/stock.html")
def stock_info():
    with open("./templates/index.html", encoding="utf-8") as f:
        content = f.read()

    my_stock_info = "这里是股票信息。。。。。。"

    content = re.sub(r"\{%content%\}", my_stock_info, content)

    return content

@route("/index.html")
def index():
    with open("./templates/index.html", encoding="utf-8") as f:
        content = f.read()

    my_stock_info = "这里是股票信息。。。。。。"

    content = re.sub(r"\{%content%\}", my_stock_info, content)

    return content

@route("/user.html")
def user_center():

    with open("./templates/center.html") as f:
        content = f.read()

    my_stock_info = "这里是个人中心，从mysql查询出来的数据。。。"

    content = re.sub(r"\{%content%\}", my_stock_info, content)

    return content

# 把path和对应的函数放在字典里
# url_func_dict = {
#     "/stock.py": stock_info,
#     "/index.py": index,
#     "/user.py":user_center
# }

def application(env, start_response):
    status = '200 OK'
    response_headers = [('Content-Type', 'text/html;charset=utf-8'),]
    start_response(status, response_headers)
    filename = env["path"] # /stock.py   /user.py

    # if filename == '/stock.py':
    #     return stock_info()
    # elif filename == '/index.py':
    #     return index()
    # elif filename == '/user.py':
    #     return user_center()
    # else:
    #     return '==你好啊!--->%s\n' % time.ctime()

    # 减少使用if else的方法
    try:
        return url_func_dict[filename]()
    except Exception as ret:
        return "产生了异常: %s " % str(ret)

