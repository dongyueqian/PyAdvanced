# _*_ coding:utf-8 _*_
import socket
"""
    本服务器与客户端通信一次后马上关闭服务
"""
def main():
    """用来完成整体的控制"""
    # 1、创建套接字
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 2、绑定IP和port
    tcp_server_socket.bind(("", 8888))

    # 3、变为监听套接字
    tcp_server_socket.listen(128)

    print("等待客户端连接......")
    # 4、等待客户端的链接
    new_socket, client_addr = tcp_server_socket.accept()
    print("客户端已连接......")

    # 5、接收客户端发送过来的请求
    recv_data = new_socket.recv(1024)
    print(recv_data)
    print(client_addr)

    # 6、给客户端返回数据
    new_socket.send("========hahha==========".encode("utf-8"))

    # 7、关闭套接字
    new_socket.close()
    tcp_server_socket.close()

if __name__ == '__main__':
    main()