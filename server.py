#!/usr/bin/env python3
# coding = utf-8

import socketserver
class MyServer(socketserver.BaseRequestHandler):

    def setup(self):
        pass

    def handle(self):
        conn=self.request

        do_parent(conn)

    def finish(self):
        pass
# 登录判断
def do_login(conn,  name, ):
    if (name in connList) or name == '管理员':
        conn.send('用户名已存在'.encode())
        return
    else:
        conn.send('OK'.encode())
        # 通知其他人欢迎进去聊天室

        msg = '\n欢迎 %s 进入聊天室' % name
        for i in connList:
            connList[i].send(msg.encode())
        # 插入用户
        connList[name] =conn

def do_namelist():
    str = 'N\n'
    for i in connList:
       str = str+'\n' +i
    for i in connList:
       connList[i].send(str.encode())

#聊天
def do_chat(conn, name, text):
    msg = '\n%s ： %s\n' % (name, text)
    for i in connList:
        connList[i].send(msg.encode())


# 退出聊天室
def do_quit(conn,  name):
    #conn.close()
    msg = name + '退出聊天室'
    for i in connList:
        if i == name:
            connList[i].close()
        else:
            connList[i].send(msg.encode())
    del connList[name]

def do_personal_chat(name,other,text):
    msg = '\n%s对您私聊说: %s\n' % (name, text)
    msg_i = '\n您对%s私聊说: %s\n' % (name, text)
    connList[other].send(msg.encode())
    connList[name].send(msg_i.encode())


# 接收客户端请求
def do_parent(conn):
    try:
        while True:
            msg = conn.recv(1024)
            msgList = msg.decode().split(' ')
            print(msgList)
            # 区分请求类型
            if msgList[0] == 'L':  # L为请求登录
                do_login(conn,  msgList[1], )
                do_namelist()
            elif msgList[0] == 'C':
                do_chat(conn,  msgList[1], ' '.join(msgList[2:]))
            elif msgList[0] == 'Q':
                do_quit(conn,  msgList[1])
                do_namelist()
            elif msgList[0] == 'P':
                do_personal_chat(msgList[1], msgList[2], ' '.join(msgList[3:]))


    except OSError:
        pass



# 创建网络,进程,调用功能函数
def main():
    # server address
    ADDR = ('127.0.0.1', 9999)
    global connList
    connList={}
    server =socketserver.ThreadingTCPServer(ADDR,MyServer)
    server.serve_forever()







if __name__ == "__main__":
    main()
