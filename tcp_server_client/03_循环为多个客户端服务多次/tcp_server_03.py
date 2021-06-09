# _*_ coding:utf-8 _*_
import socket

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
            print("等待一个新的客户端连接......")
            # 4、等待客户端的链接
            new_socket, client_addr = tcp_server_socket.accept()
            print("一个新的客户端已连接......")

            # 循环为一个客户端服务多次
            while True:
                # 5、接收客户端发送过来的请求
                recv_data = new_socket.recv(1024)
                print("客户端%s发送的请求是:%s" % (client_addr,recv_data.decode("utf-8")))

                # 如果recv解堵塞，那么有2种方式：
                # 1.客户端发送过来数据
                # 2.客户端调用close导致这里的recv解堵塞
                if recv_data :
                    # 6、给客户端返回数据
                    new_socket.send("========你好==========".encode("utf-8"))
                else:
                    break

            # 7、关闭accept返回的套接字，不再为这个客户端服务
            new_socket.close()
            print("已经为这个客户端服务完毕")
    except KeyboardInterrupt:
        # 8、关闭监听套接字
        tcp_server_socket.close()
        print("服务器关闭")

if __name__ == '__main__':
    main()