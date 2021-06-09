# _*_ coding:utf-8 _*_
import socket
import threading
"""
实现一个服务器为多个客户端循环服务多次，需要用多线程
"""

# 让子线程来为客户端服务
def dealClient(new_socket,client_addr):
    # 循环为一个客户端服务多次
    while True:
        # 5、接收客户端发送过来的请求
        recv_data = new_socket.recv(1024)

        # 如果recv解堵塞，那么有2种方式：
        # 1.客户端发送过来数据
        # 2.客户端调用close导致这里的recv解堵塞
        if recv_data:
            print("客户端%s发送的请求是:%s" % (client_addr, recv_data.decode("utf-8")))
            # 6、给客户端返回数据
            new_socket.send("========你好==========".encode("utf-8"))
        else:
            break
    # 关闭accept返回的套接字，不再为这个客户端服务
    print("为%s服务结束" % (client_addr,))
    new_socket.close()

def main():
    """用来完成整体的控制"""
    # 1、创建套接字
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 2、绑定IP和port
    tcp_server_socket.bind(("", 8888))
    # 3、变为监听套接字
    tcp_server_socket.listen(128)

    try:
        # 循环为多个客户端服务
        while True:
            # print("等待一个新的客户端连接......")
            # 4、等待客户端的链接
            new_socket, client_addr = tcp_server_socket.accept()
            print("%s已连接......" % (client_addr,))

            # 5、创建一个子线程用来处理与客户端之间的通信
            t = threading.Thread(target=dealClient, args=(new_socket,client_addr))
            t.start()

    except KeyboardInterrupt:
        # 8、关闭监听套接字
        tcp_server_socket.close()
        print("服务器关闭")

if __name__ == '__main__':
    main()