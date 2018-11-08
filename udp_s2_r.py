from socket import *
import time
from time import ctime
import os
import _thread
import re
id_passwd={}
ip_id={}
ip_sign={}

p_num=0
live_num=0
id_get_sign=1
#状态机
#客户端
#登录  新注册
#公聊 私聊
#退出

#new-one:2  sign:1
#sign ok,new ok :4
#select a b save in 4

#第一级
def account_deal(udp_s,addr,data):#一级分支，决定账号
    
    global id_passwd
    global ip_id
    global ip_sign
    global p_num
    global live_num
    global id_get_sign
    chat_ip={}
    f_ip,f_port=addr
    addr=(f_ip,13142)
    if f_ip in ip_sign.keys():
        if ip_sign[f_ip]==1:#登录验证部分
            id_num,passwd=data.split()
            if sign_in(id_num,passwd):
                live_num=live_num+1
                msg='you are ok---'+str(live_num)+'---online'
                ip_sign[f_ip]=4
                ip_id[f_ip]=id_num
                for tt in ip_id.keys():
                    msg1='you can chat with'+'\n '+str(ip_id[tt])+'\n'
                msg=msg+msg1
                udp_s.sendto(msg.encode(encoding='utf-8'),addr)
            else:
                msg='id or passwd error'
                udp_s.sendto(msg.encode(encoding='utf-8'),addr)
        elif ip_sign[f_ip]==4:
            if data=='a':
                msg='all chat successful'
                udp_s.sendto(msg.encode(encoding='utf-8'),addr)
                ip_sign[f_ip]=5
            elif data=='save':
                msg='save successful'
                udp_s.sendto(msg.encode(encoding='utf-8'),addr)
                user_save()
            elif data=='aleft':
                msg='you have went sleep '
                udp_s.sendto(msg.encode(encoding='utf-8'),addr)
                live_num=live_num-1
                del ip_id[f_ip]
                del ip_sign[f_ip]
            
            else:
                try:
                    mod,chat_id=data.split()
                    ip_sign=6
                    for y in ip_id.keys():
                        if chat_id==ip_id[y]:
                            chat_ip[f_ip]=y
                            msg='start chat with'+str(chat_id)
                            udp_s.sendto(msg.encode(encoding='utf-8'),addr)
                except:
                    msg='error'
                    udp_s.sendto(msg.encode(encoding='utf-8'),addr)
        elif ip_sign[f_ip]==5:#公聊状态
            if data!='left':
                msg='send successful'
                udp_s.sendto(msg.encode(encoding='utf-8'),addr)
                for z in ip_id.keys():
                    if z!=f_ip:
                        data=data+' from:'+str(ip_id[f_ip])
                        ip=z
                        send_addr=(ip,13142)
                        udp_s.sendto(data.encode(encoding='utf-8'),send_addr)
            else:
                ip_sign[f_ip]=4
                msg='exit successfu;'
                udp_s.sendto(msg.encode(encoding='utf-8'),addr)
        elif ip_sign[f_ip]==6:#私聊状态
            if data!='left':
                data=data+'\nfrom '+str(ip_id[f_ip])
                udp_s.sendto(data.encode(encoding='utf-8'),(chat_ip[f_ip],13142))
                msg='send succeessful'
                udp_s.sendto(msg.encode(encoding='utf-8'),addr)
            else:
                msg='exit successful'
                udp_s.sendto(msg.encode(encoding='utf-8'),addr)
                ip_sign[f_ip]=4
                
        elif ip_sign[f_ip]==2:
            if len(data)<=16 and len(data)>=6:
                id_passwd[ip_id[f_ip]]=data
                ip_sign[f_ip]=4
                live_num=live_num+1
                msg='欢迎你，新用户\nand now---'+str(live_num)+'---online\n'
                msg1='you can chat with'+'\n '
                msg2=' '
                for one in ip_id.keys():
                    if one!=f_ip:
                        msg2=msg1+str(ip_id[one])+'\n'
                msg3=msg+msg2
                udp_s.sendto(msg3.encode(encoding='utf-8'),addr)
            else:
                msg='passwd is illlegal'
                udp_s.sendto(msg.encode(encoding='utf-8'),addr)
            
    else:#第一步
        if data=='sign':
            msg='Please input as id password'
            udp_s.sendto(msg.encode(encoding='utf-8'),addr)
            ip_sign[f_ip]=1
        elif data=='new-one':
            msg='Please input words(6-16) as password'
            #信号量操作
            wait()
            num=id_get_new()
            vit()
            msg='id:'+str(num)+'\n'+msg
            udp_s.sendto(msg.encode(encoding='utf-8'),addr)
            ip_sign[f_ip]=2
            ip_id[f_ip]=num

def send(udp_s,msg,addr):
    udp_s.sendto(msg.encode(encoding='utf-8'),addr)
    
#聊天部分
def chat_list(udp_s,addr):
    for one in ip_id.keys():
        msg='you can chat with '+str(ip_id[one])
    udp_s.sendto(msg.encode(encoding='utf-8'),addr)
def id_get_new():
    global p_num
    p_num=p_num+1
    return p_num

#信号量部分
def wait():
    global id_get_sign
    while True:
        if(id_get_sign>0):
            id_get_sign=id_get_sign-1
            break
        else:
            time.sleep(1)
def vit():
    global id_get_sign
    id_get_sign=id_get_sign+1

    
#帐号密码部分 
def id_get():
    id_create=p_num+1
    return id_create




   
def user_save(file_name='user'):#写入帐号密码
    global id_passwd
    file_name=file_name+'.txt'
    f = open(file_name,"w+")
    for one in id_passwd.keys():
        f.write(str(one)+' '+str(id_passwd[one])+'\n')
    f.close()
    return True
    
def user_get(file_name='user'):#读取账号密码
    global id_passwd
    global p_num
    file_name=file_name+'.txt'
    try:
        t=open(file_name,"a+")
        t.close()
    except:
        pass

    with open(file_name,"r+") as f:
        while True:
            lines=f.readline()
            if not lines:
                break
            id_name,passwd=lines.split()
            id_passwd[id_name]=passwd
            p_num=p_num+1
            pass
    f.close()
    return True
    
def sign_in(user_id,password):#验证帐号密码
    if user_id in id_passwd.keys():
        print(password)
        if id_passwd[user_id]==password:
            return True
        else:
            return False
    else:
        return False
    
def ip_select(f_ip):
    if addr in ip_id.keys():
        return True
    else:
        return False
    
def id_get(from_addr):
    return ip_id[from_addr]

def msg_send(udp_s,from_addr,to_addr,msg):
       msg = "at  %s  %s "%(ctime(),data)
       udp_s.sendto(msg.encode(encoding='utf-8'),addr)
    
        

if __name__=="__main__":
   user_get()
   host = '' #监听所有的ip
   port = 13141 #接口必须一致
   bufsize = 1024
   addr = (host,port)
   udp_s = socket(AF_INET,SOCK_DGRAM)
   udp_s.bind(addr) #开始监听
   while True:
       print('Waiting for connection...')
       data,(ip,port) = udp_s.recvfrom(bufsize)  #接收数据和返回地址
       #处理数据
       data  = data.decode(encoding='utf-8')
       try:
           _thread.start_new_thread(account_deal,(udp_s,(ip,port),data) )
       except:
           print ("Error: 无法启动线程")
       #发送数据
       print('from :',addr)
       print(data)
   udp_s.close()
