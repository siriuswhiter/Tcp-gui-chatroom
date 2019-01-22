# client.py

from socket import *
import sys
import threading
import wx
import easygui as g



def recv_msg():
    while True:
        data = s.recv(2048)

        if data.decode() == 'EXIT':
            sys.exit(0)

        elif data.decode().split('\n')[0] == 'N':
                global nlist
                nlist=data.decode()[2:]
        # 窗口中调用personal(other,name,text)
        ###开启聊天窗口==
                nlist = '在线用户:\n' + nlist
                contact_text.SetValue(nlist)
        else:
            content_text.AppendText(data.decode())


def nameListPoll():
    msg='N '
    s.send(msg.encode())

def send_pri_msg(event):
    name = name_text.GetValue()
    text = msg_text.GetValue()

    msg = 'P '+name+' '+text
    msg_text.SetValue(msg)
    send_msg(msg_text)



def send_msg(event):
    text = msg_text.GetValue()
    if text.split(' ')[0]=='P':
        p='P'
        other=text.split(' ')[1]
        arry=text.split(' ')
        text=text[4:]
        msg = p + ' %s %s %s' % (name,other , text)
    else:
        p='C'
        msg = p + ' %s %s' % (name, text)
    try:
        msg = msg.encode()
        s.send(msg)
        msg_text.Clear()

    except:
        msg = "Q " + name
        s.send(msg.encode())
        s.close()
        sys.exit("退出聊天室")

def do_quit(event):
    frame.Destroy()
    msg = "Q " + name
    s.send(msg.encode())
    s.close()
    sys.exit("退出聊天室")




s = socket(AF_INET,SOCK_STREAM)

HOST = "127.0.0.1"
PORT = 9999
ADDR = (HOST, PORT)
s.connect(ADDR)
# 创建套接字


app = wx.App()
frame = wx.Frame(None, title="聊天室", pos=(400, 200), size=(500, 400))
panel = wx.Panel(frame)
frame.Bind(wx.EVT_CLOSE,do_quit)

msg_text = wx.TextCtrl(panel)
name_text = wx.TextCtrl(panel)

msg_button = wx.Button(panel, label="发送")
msg_button.Bind(wx.EVT_BUTTON, send_msg)

private_button = wx.Button(panel, label="私聊")
private_button.Bind(wx.EVT_BUTTON, send_pri_msg)



content_text = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
content_text.SetValue(' ')
contact_text = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
contact_text.SetValue('在线用户：\n\n ')

box = wx.BoxSizer()
box.Add(private_button, proportion=1, flag=wx.EXPAND | wx.ALL, border=3)
box.Add(name_text, proportion=1, flag=wx.EXPAND | wx.ALL, border=3)
box.Add(msg_text, proportion=20, flag=wx.EXPAND | wx.ALL, border=3)
box.Add(msg_button, proportion=2, flag=wx.EXPAND | wx.ALL, border=3)


c_box = wx.BoxSizer()
c_box.Add(content_text, proportion=10, flag=wx.EXPAND | wx.ALL, border=3)
c_box.Add(contact_text, proportion=2, flag=wx.EXPAND | wx.ALL, border=3)


v_box = wx.BoxSizer(wx.VERTICAL)
v_box.Add(c_box, proportion=10, flag=wx.EXPAND | wx.ALL, border=3)
v_box.Add(box, proportion=1, flag=wx.EXPAND | wx.ALL, border=3)

panel.SetSizer(v_box)



while True:
    name = g.enterbox(msg='请输入聊天昵称:')
    msg = 'L ' + name

    s.send(msg.encode())
    # 等待服务器回复
    data = s.recv(1024)
    if data.decode() == 'OK':
        content_text.AppendText('您已进入聊天室')
        break
    else:
        # 不成功服务器会回复不允许登录的原因
        g.msgbox("                                  昵称已被占用!", ok_button="重新输入")

th1 = threading.Thread(target=recv_msg)
th1.setDaemon(True)
th1.start()




frame.Show()
app.MainLoop()













