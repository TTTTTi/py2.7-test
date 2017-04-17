# -*- coding:utf-8 -*-
import socket
import threading
import sys

con = threading._Condition() #条件
host = raw_input('input the server ip address')
port = 8888
data = ''
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)#创建套接字
print 'Socket created'
s.bind((host,port))#把套接字绑定IP地址
s.listen(5)
print 'SOcket now listening'

#接收
def ClientThreadIN(conn,nick):
    global data
    while True:
        try:
            temp = conn.recv(1024)#客户端发过来的消息
            if not temp:
                conn.close()
                return
            NotifyALl(temp)
            print data

        except:
            NotifyALl(nick+'leaves the room')#退出
            print data
            return

#发送
def ClientThreadOut(conn, nick):
     global data
     while True:
         if con.acquire():
             con.wait()
             if data:
                 try:
                     conn.send(data)
                     con.release()
                 except:
                     con.release()
                     return


def NotifyALl(ss):
    global data
    if con.acquire():#获取锁
        data = ss
        con.notifyAll()#当前线程放弃对资源占有，通知所有等待线程从wait方法执行
        con.release()




while True:
    conn, addr = s.accept()#接受连接
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
    nick = conn.recv(1024)#获取用户名
    NotifyAll('Welcome ' + nick + ' to the room!')
    print data
    print str((threading.activeCount() + 1) / 2) + ' person(s)!'#当前房间的人数
    conn.send(data)
    threading.Thread(target = clientThreadIn , args = (conn, nick)).start()
    threading.Thread(target = ClientThreadOut , args = (conn, nick)).start()

s.close()