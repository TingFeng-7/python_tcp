from socket import *
import random,sys

#HOST = '127.0.0.1'
Server_addr = ('127.0.0.1',8880)
tcpServer = socket(AF_INET,SOCK_STREAM)   #区别UDP是Stream流传输,创建套接字

#1.判断奇偶
def oe(s):         
    if (s%2) == 0:
        return 0
    else:
        return 1
#2.扔骰子
def random_dice():     
    n = random.randint(1,6)#随机返回1-6范围内的一个整数，包括边界
    return str(n)
#3.循环发骰子,返回点数记录
def roll_send(sc,len):
    a=[]
    for m in range(len):
        m = random_dice()
        sc.send(m.encode('utf-8'))    #TCP使用send，因为tcp基于连接，故不需要指定地址。发四次
        print(m)
        a.append(m)
    return a
#4.生成这局赢家type
def judge_dice(n1,n2,n3,n4):     #该局结果
    if (n1==an1) and (n2==an2): #1.头彩，第一个对于第一个，第二个对应第二个
        return 'tc'
    elif ((n1==an1)and(n2==an2))or((n1==an2)and(n2==an1)):#2.大彩顺序可颠倒
        return 'dc
    elif (an1!=an2) and (oe(an1)==0) and (oe(an2)==0):#3.空盘，自己的an1，不一样
        return 'kp'
    elif ((an1+an2)==7):#4.七星，既加起来是7
        return 'qx'
    elif (oe(an1)==1) and (oe(an2)==1):#5.单对，两奇数
        return 'dd'
    elif ((an1+an2)==3)or((an1+an2)==5)or((an1+an2)==9)or((an1+an2)==11):#6.散星
        return 'sx'
    else:#从服务端，这种情况不存在
        return '没有该种点型！'
        sys.exit()

tcpServer.bind(Server_addr)       #绑定地址（端口号）
tcpServer.listen(500)    #设置监听（最大连接数）

##循环接收数据
while True:
    print('RemoteBet {}'.format(’127.0.0.1‘))
    #等待客户端的连接，accept()函数return一个二元组
    sc, sc_addr = tcpServer.accept()#sc为客户端的socket对象，sc_addr为客户端的地址(ip地址，端口号)
    print('{} 加入了游戏'.format(sc_addr))        #记录玩家信息
    while True:
        1st=roll_send(sc,2)#庄家先叫两个
        data = sc.recv(1024).decode('utf-8')  #玩家要叫骰子，所以要接受数据
        2rd=roll_send(sc,2)#先收到，再发两个判断骰
        if not data or data == 'exit':
            sys.exit()
        print('玩家{}说：'.format(sc_addr)+data)  #玩家结果
        yaType=data.split(' ')[1]
        print(yaType)
        #把列表拼起来 ,,,,算出这局赢的点型
        r=1st+2rd
        if yaType==(judge_dice(r[0],r[1],r[2],r[3])):
            sc.send(b'win')
        else:
            sc.send(b'lose')
        print('已发送')
    sc.close()
tcpServer.close()                 #关闭套接字
