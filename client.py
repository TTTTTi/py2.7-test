# -*- coding: utf-8 -*-

import socket
import  threading

nick = raw_input('input your nickname')
ip = raw_input("input the server ip address:")

outString = ''
inString = ''
nike = ''


# 发送信息函数
def DealOut(sock):
    global nick, outString
    while True:
        outString = raw_input()  # 输入才停
        outString = nike + ':' + outString  # 拼接
        sock.send(outString)  # 发送


# 接收信息函数
def DealIn(sock):
    global inString
    while True:
        try:
            inString = sock.recv(1024)
            if not inString:
                break

            if outString != inString:
                print inString
        except:
            break


nick = raw_input('input your nickname')
ip = raw_input("input the server ip address:")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建套接字
sock.connect((ip, 8888))  # 发起请求
sock.send(nick)

# 多线程
thin = threading.Thread(target=DealIn(), args=(sock,))  # 创建接收信息线程
thin.start()
shout = threading.Thread(target=DealOut(), args=(sock,))  # 创建发送信息线程
thin.start()
