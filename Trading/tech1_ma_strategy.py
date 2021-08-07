#%%
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime 
import os.path 
import sys  
import pyfolio
import backtrader as bt
# 建立一個backtrader回測框架
class TestStrategy(bt.Strategy):
    #設置sma的參數，根據官方照此設置可進行暴力演算，得知何種參數最佳
    params = (
        ('fast_period', 3),
        ('slow_period', 60),
    )

    #這裡是log，當交易發生時呼叫log函數可以將交易print出來
    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    #init定義你會用到的數據
    def __init__(self):
        #呼叫close序列備用
        self.dataclose = self.datas[0].close
        #追蹤order、buyprice跟buycomm使用，可用可不用
        self.order = None
        self.buyprice = None
        self.buycomm = None
        #定義5ma跟60ma
        self.sma1 = bt.ind.SimpleMovingAverage(self.datas[0].close,period=self.params.fast_period)  
        self.sma2 = bt.ind.SimpleMovingAverage(self.datas[0].close,period=self.params.slow_period)  
        #使用bt.ind.CrossOver方法判斷兩條線的穿越關係
        self.crossover = bt.ind.CrossOver(self.sma1, self.sma2)  
    #notify_order當每次有訂單由next偵測出來的條件送出時，會觸發notify_order，好處是顯示出訂單執行的狀況以及偵測是否有資金不足的情況
    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            #當訂單為提交狀態時則不做任何事
            return

        # 當訂單完成時，若為Buy則print出買入狀況；反之亦然
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

        # 當因策略取消或是現今不足訂單被拒絕等狀況則print出訂單取消
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        #完成該有的提醒之後則將oder設置回None
        self.order = None

    #notify_trade交易通知，預設如果有倉在手就不做事，如果執行賣出則print出獲利
    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))
    #next可以把它想像成一個內建的for loop，他把數據打包好供我們使用
    def next(self):
        # print出每日收盤價
        self.log('Close, %.2f' % self.dataclose[0])
        # 檢查有無pending的訂單
        if self.order:
            return

        #有無倉位在手，如果無代表
        
        if not self.position:
             # cross over>0意味著向上穿越
            if self.crossover>0:
                
                # 紀錄買單提交
                self.log('BUY CREATE, %.2f' % self.dataclose[0])
                # 買進
                self.order = self.buy()    
                
        else:
            if self.crossover<0:
                # 紀錄賣單提交
                self.log('SELL CREATE, %.2f' % self.dataclose[0])
                # 賣出
                self.order = self.sell()
    #回測終止時print出結果
    # def stop(self):
    #     print(f'Fast MA: {self.params.fast_period} | Slow MA: {self.params.slow_period} | End Value: {self.broker.getvalue()}')

if __name__ == '__main__':
    # 創建框架
    cerebro = bt.Cerebro()
    # # 放入策略
    cerebro.addstrategy(TestStrategy)
    # # 放入策略
    # strats = cerebro.optstrategy(
    #     TestStrategy,
    #     fast_period = range(3, 7), 
    #     slow_period = range(40, 70, 10))
    # 使用框架的資料取得函數
    data = bt.feeds.YahooFinanceData(
        dataname='2330.TW',
        # 開始日期
        fromdate=datetime.datetime(2014, 1, 1),
        # 結束日期
        todate=datetime.datetime(2020, 12, 31),
        reverse=False)
    # 將datafeed餵入框架
    cerebro.adddata(data)
    # 設置起始金額
    cerebro.broker.setcash(1000000.0)
    #設置一次購買的股數，台股以1000股為主
    cerebro.addsizer(bt.sizers.SizerFix, stake=1000) 
    # 設置傭金，稍微設置高一點作為滑價付出成本
    cerebro.broker.setcommission(commission=0.0015)
    # print出起始金額
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    # 執行策略
    cerebro.addanalyzer(bt.analyzers.PyFolio, _name='pyfolio')
    # Run over everything
    results = cerebro.run()
    # Print out the final result
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    strat = results[0]
    pyfoliozer = strat.analyzers.getbyname('pyfolio')
    returns, positions, transactions, gross_lev = pyfoliozer.get_pf_items()
  
    # # pyfolio showtime
    import pyfolio as pf
    pf.create_full_tear_sheet(
    returns,
    positions=positions,
    transactions=transactions,
    live_start_date='2018-01-01')  # This date is sample specific)
# %%
