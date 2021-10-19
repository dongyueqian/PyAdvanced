import re
import pymysql
import urllib.parse
from logs.logger import logger

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

@route(r"/index.html")
def index(ret):
    return stock_info(ret)

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
    cursor.execute("select * from fund_info;")

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
    cursor.execute("select i.code, i.name, i.jzzzl, i.type,i.dwjz,i.ljjz,f.note_info from fund_info i inner join fund_focus f on i.id = f.info_id;")

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
                <a type="button" class="btn btn-default btn-xs" href="/update/%s.html"> <span class="glyphicon glyphicon-star" aria-hidden="true"></span> 修改 </a>
            </td>  
            <td>
                <input type="button" value="删除" id="toDel" name="toDel" systemidvaule="%s">
            </td>  
        </tr>
    """
    html = ""
    for items in my_stock_info:
        html += datas % (items[0], items[1], items[2], items[3],
                         items[4], items[5], items[6],items[0],items[0])
    content = re.sub(r"\{%content%\}", html, content)

    return content

@route(r"/add/(\d+)\.html")
def add_focus(ret):
    """ 添加关注 """
    # 1、从分组中得到代码stock_code
    stock_code = ret.group(1)

    # 2、判断stock_code是否存在
    # 打开数据库连接
    conn = pymysql.connect(host="localhost", user="root", password="12345678", database="stock_db", charset="utf8")
    # 使用cursor()方法创建一个游标对象cursor
    cursor = conn.cursor()
    # 使用execute()方法执行sql查询
    sql = "select * from fund_info where code=%s;"
    cursor.execute(sql, (stock_code,))
    # 如果所添加的stock_code不存在（在我的数据库中没有这个代码）
    if not cursor.fetchone():
        # 关闭数据库连接
        cursor.close()
        conn.close()
        logger.warning("搜索的基金代码不存在")
        return "抱歉，您搜索的基金代码不存在哦～"

    # 3、判断stock_code是否已经关注
    sql = "select * from fund_info i inner join fund_focus f on i.id = f.info_id where i.code=%s"
    cursor.execute(sql, (stock_code,))
    if cursor.fetchone():
        # 关闭数据库连接
        cursor.close()
        conn.close()
        logger.warning("%s已在您的关注列表中，请勿重复关注" % stock_code)
        return "%s已在您的关注列表中，请勿重复关注" % stock_code

    # 4、基金代码存在，且未关注，则该基金添加进关注列表
    sql = "insert into fund_focus (info_id) select id from fund_info where code=%s"
    cursor.execute(sql, (stock_code,))
    conn.commit() # 提交事物

    return "add  %s ok ...." % stock_code

@route(r"/del/(\d+)\.html")
def del_focus(ret):
    """ 取消关注 """
    # 1、从分组中得到代码stock_id
    stock_code = ret.group(1)

    # 2、判断stock_code是否存在
    # 打开数据库连接
    conn = pymysql.connect(host="localhost", user="root", password="12345678", database="stock_db", charset="utf8")
    # 使用cursor()方法创建一个游标对象cursor
    cursor = conn.cursor()
    # 使用execute()方法执行sql查询
    sql = "select * from fund_info where code=%s;"
    cursor.execute(sql, (stock_code,))
    # 如果所添加的stock_code不存在（在我的数据库中没有这个代码）
    if not cursor.fetchone():
        # 关闭数据库连接
        cursor.close()
        conn.close()
        logger.warning("搜索的基金代码不存在")
        return "抱歉，您搜索的基金代码不存在哦～"

    # 3、判断stock_code是否已经关注
    sql = "select * from fund_info i inner join fund_focus f on i.id = f.info_id where i.code=%s"
    cursor.execute(sql, (stock_code,))
    # 如果没有关注
    if not cursor.fetchone():
        # 关闭数据库连接
        cursor.close()
        conn.close()
        logger.warning("您未关注%s" % stock_code)
        return "您未关注%s" % stock_code

    # 4、基金代码存在，且已关注，则从关注列表中删除次代码
    sql = "delete from fund_focus where info_id=(select id from fund_info where code=%s)"
    cursor.execute(sql, (stock_code,))
    conn.commit() # 提交事物

    return "del %s ok ...." % stock_code

@route(r"/update/(\d+)\.html")
def update_page(ret):
    """ 修改备注信息,显示修改备注的页面 """

    # 1、从分组中得到代码stock_code
    stock_code = ret.group(1)

    # 2、打开资源
    with open("./templates/update.html") as f:
        content = f.read()

    # 3、判断stock_code是否存在
    # 打开数据库连接
    conn = pymysql.connect(host="localhost", user="root", password="12345678", database="stock_db", charset="utf8")
    # 使用cursor()方法创建一个游标对象cursor
    cursor = conn.cursor()
    # 使用execute()方法执行sql查询
    sql = "select * from fund_info where code=%s;"
    cursor.execute(sql, (stock_code,))
    # 如果所添加的stock_code不存在（在我的数据库中没有这个代码）
    if not cursor.fetchone():
        # 关闭数据库连接
        cursor.close()
        conn.close()
        logger.warning("搜索的基金代码不存在")
        return "抱歉，您搜索的基金代码不存在哦～"

    # 4、判断stock_code是否已经关注
    sql = "select * from fund_info i inner join fund_focus f on i.id = f.info_id where i.code=%s"
    cursor.execute(sql, (stock_code,))
    if not cursor.fetchone():
        # 关闭数据库连接
        cursor.close()
        conn.close()
        logger.warning("%s不在您的关注列表中，无法操作" % stock_code)
        return "%s不在您的关注列表中，无法操作" % stock_code

    # 5、基金代码存在，且在关注列表中，则显示该基金的信息
    sql = "select note_info from fund_focus where info_id = (select id from fund_info where code=%s)"
    cursor.execute(sql, (stock_code,))
    stock_mark_info = cursor.fetchone() # stock_mark_info是元组
    # 关闭数据库连接
    cursor.close()
    conn.close()

    content = re.sub(r"\{%note_info%\}", str(stock_mark_info[0]), content)
    content = re.sub(r"\{%code%\}", stock_code, content)

    return content


@route(r"/update/(\d+)/(.*)\.html")
def save_mark(ret):
    """ 修改备注信息,显示修改备注的页面 """

    # 1、从分组中得到代码stock_code和备注信息mark_info
    stock_code = ret.group(1)
    # 把页面的数据解码
    mark_info = urllib.parse.unquote(ret.group(2))

    # 2、打开数据库连接
    conn = pymysql.connect(host="localhost", user="root", password="12345678", database="stock_db", charset="utf8")
    # 使用cursor()方法创建一个游标对象cursor
    cursor = conn.cursor()
    sql = "update fund_focus set note_info=%s where info_id = (select id from fund_info where code=%s)"
    # 解码后的数据提交到数据库
    cursor.execute(sql, (mark_info, stock_code))
    conn.commit()
    # 关闭数据库连接
    cursor.close()
    conn.close()

    return "修改成功"

def application(env, start_response):
    status = '200 OK'
    response_headers = [('Content-Type', 'text/html;charset=utf-8'),]
    start_response(status, response_headers)
    filename = env["path"] # /stock.html   /user.html
    method = env["method"] # post get

    # if filename == '/stock.py':
    #     return stock_info()
    # elif filename == '/index.py':
    #     return index()
    # elif filename == '/user.py':
    #     return user_center()
    # else:
    #     return '==你好啊!--->%s\n' % time.ctime()

    try:
        # return url_func_dict[filename]()
        for url, func in url_func_dict.items():
            ret = re.match(url,filename)
            if ret:
                # print("请求路径：",filename)
                # print("这个是个%s方法" % method)
                logger.debug(f"请求路径: {filename}")
                return func(ret)
        else:
            logger.debug(f"请求路径: {filename}")
            logger.warning("您请求的URL(%s)没有对应的函数" % filename)
            return "您请求的URL(%s)没有对应的函数" % filename

    except Exception as ret:
        logger.error(f"产生了异常: {str(ret)}")
        return "产生了异常: %s " % str(ret)