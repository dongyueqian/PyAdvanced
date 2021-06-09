# _*_ coding:utf-8 _*_
import socket

def main():
    """用来完成整体的控制"""
    # 1、创建套接字
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 2、链接服务器
    # server_ip = input("请输入要连接的服务器IP地址：")
    # server_port = int(input("请输入要连接的服务器端口号："))
    # server_addr = (server_ip,server_port)
    server_addr = (("192.168.0.102", 8888))
    tcp_server_socket.connect(server_addr)

    while True:
        # 3、发送数据/接收数据
        send_data = input("请输入要发送的数据：")
        tcp_server_socket.send(send_data.encode("utf-8"))

    # 4、关闭套接字
    tcp_server_socket.close()

if __name__ == '__main__':
    main()