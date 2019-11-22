from socket import *
import sys


#1.建立tcp套接字,连接server端
Server_addr = ('127.0.0.1',8880)
client = socket(AF_INET,SOCK_STREAM)
client.connect(Server_addr)              

#1.规则描述
dd= {'tc': '押头彩:两束顺序点数均正确xx1:35', 'dc': '押大彩:两束点数正确xx1:17',
'kp' : '押空盘:两数不同且均为偶数xx1:5', 'qx' :'押七星:两数之和为七xx1:5',
'dd': '押单对:两数均为奇数xx1:3' ,'sx' : '押散星:两数之和为三、五、九、十一xx1:2'}
#2.赔率表声明
keys=[]
rate=[]
#1-1.规则介绍
print('-------------------------------------------')
print('欢迎来到风月赌场,规则如下：')
for key in dd.keys():#遍历key就好
    val=dd[key].split('xx')
    print('ya {} <数量> <coin|silver|gold> {:<20s} {:6s}'.format(key,val[0],val[1]))
    keys.append(key)
    rate.append(val[1])
#2-1.赔率表出来了
rate_dict=zip(keys,rate)

#骰子图样字典 三个单引号
dict1 = {'1':'''              
          ┌───┐
          │   │
          │ ● |
          │   │
          └───┘
          ''',
         '2':''''
          ┌───┐
          │ ● │
          │   │
          │ ● │
          └───┘
          ''',
         '3':'''
          ┌───┐
          │ ● │
          │   │
          │● ●│
          └───┘
          ''',
         '4':'''
          ┌───┐
          │● ●│
          │   │
          │● ●│
          └───┘
          ''',
         '5':'''
          ┌───┐
          │● ●│
          │ ● │
          │● ●│
          └───┘
          ''',
         '6':'''
          ┌───┐
          │● ●│
          │● ●│
          │● ●│
          └───┘
          '''
                }
dict2 = {'1':'一','2':'二','3':'三','4':'四','5':'五','6':'六'}       #骰子点数字典

#个人微金库类创建
class vibank:
    #1.汇率比例
    coin = 1
    silver = 10 * coin
    gold = 100 * coin
    balance = 100
    #2.记录押注金额和类型
    bet = coin #default,初始一coin
    mode = '' #tc,dc,dd,sd,sx
    csg='' #coin silver,gold

    #重新设置
    def set_init(self,bet,typ,csg):
        self.bet=bet
        self.mode=typ
        self.csg=csg

    #4.计算余额,下注类型出来
    def compute(self,flag):
        # global rate_dict
        # er=rate_dict[self.mode] er是汇率 
        rate=17
        if self.csg=='coin':
            er=self.coin
        elif self.csg=='silver':
            er=self.silver
        else:
            er=self.gold
        #货币单位调整完毕，押数x赔率x汇率
        if flag=='win':
            self.balance+=self.bet*er*rate
        else:
            self.balance-=self.bet*er*rate
        print('您的余额是:{}'.format(self.balance))    
        self.bet=1  #default=1

customer=vibank()
#循环是为了保证能持续进行通话
#Zhen
while True:
    print("""
        庄家唱道：新开盘！预叫头彩！
        庄家将两枚玉骰往银盘中一撒。
        """)
    global n1,n2,an1,ya
    n1 = (client.recv(1).decode('utf-8'))   # 因为1个数字只占一个字节，接受服务器端发来的点数
    n2 = (client.recv(1).decode('utf-8'))
    print(dict1[n1],dict1[n2])         #输出对应点数的预备字典
    print('庄家唱道：头彩骰号是 {}、{}'.format(dict2[n1],dict2[n2]))
    data = input('输入你押的值  (ya <玩法> <数量> <coin|silver|gold>) ：')#ya dd 2 coin
    ##分析data
    if data != 'exit':     #
        client.send(data.encode('utf-8'))
        line=data.split(' ')#储存押注类，然后再完成化
        customer.set_init(line[1],line[2],line[3])
    else:                               
        client.send(data.encode('utf-8'))#唯一send
        sys.exit()

    ##准备接收点数
    print("""
        庄家将两枚玉骰扔进两个金盅，一手持一盅摇将起来。
        庄家将左手的金盅倒扣在银盘上，玉骰滚了出来。""")
    an1 = (client.recv(1).decode('utf-8'))
    print(dict1[an1])
    print("""
        庄家将右手的金盅倒扣在银盘上，玉骰滚了出来。""")
    bn2 = (client.recv(1).decode('utf-8'))
    print(dict1[bn2])
    ###接受，庄家判输赢
    result=client.recv()
    print('庄家叫道：{}、{}'.format(dict2[an1],dict2[bn2]))
    customer.compute(result)
   #金库情况