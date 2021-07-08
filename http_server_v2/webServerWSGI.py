# coding=utf-8
import socket
import re
import multiprocessing
import miniFrameWSGI

"""
运行脚本，在浏览器输入：http://127.0.0.1:8888/index.html 并回车
将在浏览器看到相应的页面
"""
class WSGIServer(object):

    def __init__(self):
        # 1、创建套接字
        self.http_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 设置当服务器先close 即服务器端4次挥手之后资源能够立即释放，这样就保证了，下次运行程序时 可以立即绑定8888端口
        self.http_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # 2、绑定IP和port
        self.http_socket.bind(("", 8888))
        # 3、变为监听套接字
        self.http_socket.listen(128)

    def dealHttpRequest(self,new_socket):
        # 接收浏览器发送过来的数据
        requests = new_socket.recv(1024).decode("utf-8")
        # print(">"*80)
        # print(requests)

        request_lines = requests.splitlines()
        # print("")
        print(">"*80)
        print(request_lines)

        # 提取请求内容：'GET /ziyuan.html HTTP/1.1'
        ret = re.match(r"[^/]+(/[^ ]*)",request_lines[0])
        file_name = ''
        if ret:
            file_name = ret.group(1)
            if file_name == "/":
                file_name = "/index.html"
            print("*"*50,file_name)

        # 如果请求的资源不是以.py结尾，就认为是静态资源：html,css, js,png等
        if not file_name.endswith(".py"):
            try:
                # 正常打开文件文件
                f = open("./html" + file_name ,"rb")

            except:  # 打开文件失败，即 找不到用户输入的文件名，执行以下内容，也要给浏览器返回数据
                response = "HTTP/1.1 404 NOT FOUND\r\n"
                response += "\r\n"
                response += "------404 NOT FOUND------"
                new_socket.send(response.encode("utf-8"))

            else:
                # 打开文件成功执行以下内容，html_content是要发送的body
                html_content = f.read()
                f.close()

                # 准备发送给浏览器的header
                response = "HTTP/1.1 200 OK\r\n"
                response += "\r\n"

                # 准备发送给浏览器的body
                # response += "<h1>Hello World!</h1>"

                # 将response header发送给浏览器
                new_socket.send(response.encode("utf-8"))

                # 将response body发送给浏览器
                new_socket.send(html_content)

        # 如果是以.py结尾，就认为是动态资源
        else:
            env = {}
            # 调用框架的函数,拿到body
            body = miniFrameWSGI.application(env,self.start_response)

            # 准备发送给浏览器的header
            response = "HTTP/1.1 %s\r\n" % self.status
            for temp in self.response_headers:
                response += "%s:%s\r\n" % (temp[0],temp[1])
            response += "\r\n"
            response += body
            # 将response header和body发送给浏览器
            new_socket.send(response.encode("utf-8"))

        # 关闭套接字
        new_socket.close()

    def start_response(self,status,response_headers):
        self.status = status
        self.response_headers = response_headers

    def run(self):
        while True:
            # 等待浏览器的连接
            new_socket, http_request_addr = self.http_socket.accept()

            # 处理浏览器的请求
            # self.dealHttpRequest(new_socket)
            # 用多进程实现处理浏览器的请求
            p = multiprocessing.Process(target=self.dealHttpRequest, args=(new_socket,))
            p.start()
            # 多进程，进程之间不共享资源，需要关闭套接字
            new_socket.close()

    def __del__(self):
        self.http_socket.close()
        print("关闭套接字")

def main():
    # 控制整体，创建一个web服务器对象，然后调用这个对象的run方法
    wsgi_server = WSGIServer()
    try:
        wsgi_server.run()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()