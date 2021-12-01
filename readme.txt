1、author：dongyueqian
   email：874974405@qq.com

2、运行方式：
    在命令行输入 ./run.sh
    或者
    python3 webServerWSGI.py 8888 miniFrameWSGI:application

    在浏览器输入：http://127.0.0.1:8888/index.html，进行访问
   
    

3、项目说明：首页展示所有基金信息，可以添加自选。个人中心展示所有添加自选的基金信息，删除自选，修改备注信息

          这是一个符合WSGI（Web服务器网关接口）标准的miniweb框架，用户在浏览器输入要访问的url，回车之后向web服务器发送请求
          web服务器判断请求的资源类型，若是请求静态资源则直接返回给浏览器，若请求是动态资源，需要调用web框架，拿到web框架返回的
          数据，web服务器再将这些数据给到浏览器

          webServerWSGI.py : web服务器，处理浏览器的请求

          dynamic/miniFrameWSGI.py : web框架，用来处理动态请求,它定义了一个符合WSGI标准的一个HTTP处理函application()
          它接收两个参数：env：一个包含所有HTTP请求信息的dict对象；start_response：一个发送HTTP响应的函数。
          整个application()函数本身没有涉及到任何解析HTTP的部分，也就是说，把底层web服务器解析部分和应用程序逻辑部分进行了分离

          sql : 本项目的数据库，使用的库名称为stock_db， 需要建2张表，使用source命令先执行fund_info.sql，再执行fund_focus.sql
                fund_focus.info_id和fund_info.id做了外键关联

          get_funds/get_funds_code.py : 爬取基金信息，处理后将基金代码写入./基金代码爬取/fundcode.csv
          get_funds/funds_insert_mysql.py : 根据基金代码查询基金其他信息，处理数据后插入mysql

          static : js 、css等静态文件
          templates : html文件

4、其他
    目前的功能: 所有数据在前端显示，添加到关注（添加到个人中心），取消关注（从个人中心删除），修改备注
    待实现的功能：1、分页  2、前端输入基金代码进行查询

