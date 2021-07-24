import re
import pymysql

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

@route(r"/stock.html")
def stock_info(ret):
    with open("./templates/index.html", encoding="utf-8") as f:
        content = f.read()

    # my_stock_info = "这里是股票信息。。。。。。"
    # content = re.sub(r"\{%content%\}", my_stock_info, content)

    # 打开数据库连接
    conn = pymysql.connect(host="localhost", user="root", password="12345678", database="stock_db", charset="utf8")

    # 使用cursor()方法创建一个游标对象cursor
    cursor = conn.cursor()

    # 使用execute()方法执行sql查询
    cursor.execute("select * from info;")

    # 使用fetchall()方法获取所有数据
    my_stock_info  = cursor.fetchall()
    # 关闭数据库连接
    cursor.close()
    conn.close()

    datas = """
        <tr>
            <th>%d</th>
            <th>%s</th>
            <th>%s</th>
            <th>%s</th>
            <th>%s</th>
            <th>%s</th>
            <th>%s</th>
            <th>%s</th>
            <td>
                <input type="button" value="添加" id="toAdd" name="toAdd" systemidvaule="%s">
            </td>  
        </tr>
    """
    html = ""
    for items in my_stock_info:
        html += datas % (items[0], items[1], items[2], items[3],
                         items[4], items[5],items[6],items[7], items[1])
    content = re.sub(r"\{%content%\}", html, content)

    return content

@route(r"/index.html")
def index(ret):
    with open("./templates/index.html", encoding="utf-8") as f:
        content = f.read()

    my_stock_info = "这里是股票信息。。。。。。"

    content = re.sub(r"\{%content%\}", my_stock_info, content)

    return content

@route(r"/user.html")
def user_center(ret):

    with open("./templates/center.html") as f:
        content = f.read()

    # my_stock_info = "这里是个人中心，从mysql查询出来的数据。。。"
    # content = re.sub(r"\{%content%\}", my_stock_info, content)

    # 打开数据库连接
    conn = pymysql.connect(host="localhost", user="root", password="12345678", database="stock_db", charset="utf8")

    # 使用cursor()方法创建一个游标对象cursor
    cursor = conn.cursor()

    # 使用execute()方法执行sql查询
    cursor.execute("select i.code,i.short,i.chg,i.turnover,i.price,i.highs,f.note_info from info i inner join focus f on i.id = f.info_id;")

    # 使用fetchall()方法获取所有数据
    my_stock_info = cursor.fetchall()
    # 关闭数据库连接
    cursor.close()
    conn.close()

    datas = """
        <tr>
            <th>%s</th>
            <th>%s</th>
            <th>%s</th>
            <th>%s</th>
            <th>%s</th>
            <th>%s</th>
            <th>%s</th>
            <td>
                <input type="button" value="=>修改" id="toAlter" name="toAlter" systemidvaule="%s">
            </td>  
            <td>
                <input type="button" value="删除" id="toDel" name="toDel" systemidvaule="%s">
            </td>  
        </tr>
    """
    html = ""
    for items in my_stock_info:
        html += datas % (items[0], items[1], items[2], items[3],
                         items[4], items[5], items[6],items[6],items[0])
    content = re.sub(r"\{%content%\}", html, content)

    return content

# 把path和对应的函数放在字典里
# url_func_dict = {
#     "/stock.py": stock_info,
#     "/index.py": index,
#     "/user.py":user_center
# }

@route(r"/add/(\d+).html")
def add_focus(ret):

    stock_id = ret.group(1)

    return "add  %s ok ...." % stock_id

def application(env, start_response):
    status = '200 OK'
    response_headers = [('Content-Type', 'text/html;charset=utf-8'),]
    start_response(status, response_headers)
    filename = env["path"] # /stock.html   /user.html

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
        # return url_func_dict[filename]()
        for url, func in url_func_dict.items():
            ret = re.match(url,filename)
            print(ret)
            if ret:
                return func(ret)
        else:
            return "您访问的页面不存在...."

    except Exception as ret:
        return "产生了异常: %s " % str(ret)

