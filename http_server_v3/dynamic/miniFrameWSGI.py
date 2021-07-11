import time

import re

def index():
    with open("./templates/index.html", encoding="utf-8") as f:
        content = f.read()

    my_stock_info = "这里是股票信息。。。。。。"

    content = re.sub(r"\{%content%\}", my_stock_info, content)

    return content

def login():
    return "======这里是登录页======"

def center():

    with open("./templates/center.html") as f:
        content = f.read()

    my_stock_info = "这里是个人中心，从mysql查询出来的数据。。。"

    content = re.sub(r"\{%content%\}", my_stock_info, content)

    return content

def application(env, start_response):
    status = '200 OK'
    response_headers = [('Content-Type', 'text/html;charset=utf-8'),]
    start_response(status, response_headers)
    filename = env["path"]
    if filename == '/index.py':
        return index()

    elif filename == '/login.py':
        return login()

    elif filename == '/center.py':
        return center()
    else:
        return '==你好啊!--->%s\n' % time.ctime()