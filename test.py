class vibank:
    #1.金币换算
    coin = 1
    silver = 10 * coin
    gold = 100 * coin
    balance = 100

    #2.记录押注金额和类型1
    bet = coin #default,初始一coin
    mode = '' #tc,dc,dd,sd,sx
    csg='' #coin silver,gold

    #重新设置
    def set_init(self,bet,typ,csg):
        self.bet=bet
        self.mode=typ
        self.csg=csg

    #计算余额,下注类型出来
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

pc=vibank()
a='10'
print(int(a))
pc.set_init(int(a),'tc','coin')
pc.compute('lose')
pc.set_init(11,'tc','coin')
pc.compute('win')