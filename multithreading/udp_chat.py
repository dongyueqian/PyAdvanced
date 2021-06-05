# _*_ coding:utf-8 _*_
import socket
import threading
'''
多线程版聊天器
可以打开2个窗口
运行本程序进行聊天
'''
def send_msg(udp_socket):
    """获取键盘数据，并将其发送给对方"""
    # 1. 输入对方的ip地址
    dest_ip = input("\n请输入对方的ip地址:")
    # 2. 输入对方的port
    dest_port = int(input("\n请输入对方的port:"))
    print("======================聊天区======================")
    while True:
        # 3. 从键盘输入数据
        msg = input("\n请输入要发送的数据:")
        # 4. 发送数据
        udp_socket.sendto(msg.encode("utf-8"), (dest_ip, dest_port))


def recv_msg(udp_socket):
    """接收数据并显示"""
    while True:
        # 1. 接收数据
        recv_msg = udp_socket.recvfrom(1024)
        # 2. 解码
        recv_ip = recv_msg[1]
        recv_msg = recv_msg[0].decode("utf-8")
        # 3. 显示接收到的数据
        print(" "*30,"%s:%s" % (str(recv_ip), recv_msg))


def main():
    # 1. 创建套接字
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 2. 绑定本地信息
    myport = int(input("\n请输入自己的port:"))
    udp_socket.bind(("", myport))

    # 3. 创建一个子线程用来接收数据
    t = threading.Thread(target=recv_msg, args=(udp_socket,))
    t.start()
    # 4. 让主线程用来检测键盘数据并且发送
    send_msg(udp_socket)

if __name__ == "__main__":
    main()