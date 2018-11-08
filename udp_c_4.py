from socket import *
import _thread
from tkinter import *
from time import ctime
ip_sign=True
def msg_send(var,var_1):
    port=13141
    if ip_sign:
        host  = '127.0.0.1'#这是客户端的电脑的ip
    else:
        host =var_1.get()
         
    bufsize = 1024  #定义缓冲大小
    addr = (host,port) # 元组形式
    udp_s = socket(AF_INET,SOCK_DGRAM) #创建客户

    space=' '
    time="%s:"%(ctime())
    data=var.get()
    listb.insert(END,time+'(me)')
    listb.insert(END,'  '+data)
    listb.delete(0)
    
    entry.delete(0,END)
    data = data.encode(encoding="utf-8") 
    udp_s.sendto(data,addr) # 发送数据
    udp_s.close()

def msg_rec(port=13142):
    host  = ''#这是客户端的电脑的ip
    bufsize = 1024  #定义缓冲大小
    addr = (host,port) # 元组形式
    udp_s = socket(AF_INET,SOCK_DGRAM) #创建客户
    udp_s.bind(addr)
    time="%s:"%(ctime())
    while True:
        data,addr = udp_s.recvfrom(bufsize) #接收数据和返回地址
        listb.insert(END,time+'server')
        listb.insert(END,'  '+data.decode(encoding="utf-8"))
        listb.delete(0)
        
    udp_s.close()
def get_new(var,var_1):
    _thread.start_new_thread(msg_send,(var,var_1))

def change():
    global ip_sign
    ip_sign=False
    
if __name__=="__main__":
    send_port=13141
    rec_port=13142

    try:
    #_thread.start_new_thread(msg_send,(send_port,))
        _thread.start_new_thread(msg_rec,(rec_port,))
    except:
        print('error')
    #GUI
    root=Tk()
    root.title('udp编程')
    root.geometry('600x400+400+200')
    
    listb  = Listbox(root) 
    listb.place(x=15,y=13,width=570, height=250)
    
    listb.insert(END,'------------------------------')
    listb.insert(END,'- 输入 sign 或 new-one       -')
    listb.insert(END,'- sign :登陆                 -')
    listb.insert(END,'- new-one:创建新用户         -')
    listb.insert(END,'- a: 进入公共聊天            -')
    listb.insert(END,'- save 聊天选择保存该用户    -')
    listb.insert(END,'- left:返回聊天选择界面      -')
    listb.insert(END,'------------------------------')

    var_1=StringVar()
    entry_1=Entry(root,textvariable = var_1)
    entry_1.place(x=35,y=310,width=160,height=30)
    
    
    var=StringVar()
    entry=Entry(root,textvariable = var)
    entry.place(x=35,y=270,width=320,height=30)
    
    

    b_change = Button(text="服务器",command=change, borderwidth="2", font=("微软雅黑", 15), background="white")
    b_send = Button(text="发送",command=lambda:get_new(var,var_1), borderwidth="2", font=("微软雅黑", 15), background="white")
    #bml.bind('<KeyPress-Enter>',lambda:msg_send(var))
    #enter键绑定按钮尚未完成
    b_send.place(x=400, y=270, width=75, height=30)
    b_change.place(x=400, y=310, width=75, height=30)

 
root.mainloop()
    
