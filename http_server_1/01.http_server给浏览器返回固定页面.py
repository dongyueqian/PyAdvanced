# _*_ coding:utf-8 _*_
import socket

"""
运行脚本，在浏览器输入：http://127.0.0.1:8888 并回车
将在浏览器看到：Hello World!
"""

def dealHttpRequest(new_socket, http_request_addr):
    # 6、接收浏览器发送过来的数据
    requests = new_socket.recv(1024)
    print(requests)

    # 7、给浏览器返回数据
    response = "HTTP/1.1 200 OK\r\n"
    response += "\r\n"
    response += "<h1>Hello World!</h1>"

    # 将response header发送给浏览器
    new_socket.send(response.encode("utf-8"))
    # 8、关闭套接字
    new_socket.close()

def main():
    # 1、创建套接字
    http_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    # 2、绑定IP和port
    http_socket.bind(("",8888))

    # 3、变为监听套接字
    http_socket.listen(128)
    try:
        while True:
            # 4、等待浏览器的连接
            new_socket, http_request_addr = http_socket.accept()

            # 5、处理浏览器的请求
            dealHttpRequest(new_socket, http_request_addr)
    except KeyboardInterrupt:
        # 9、关闭监听套接字
        http_socket.close()

if __name__ == '__main__':
    main()