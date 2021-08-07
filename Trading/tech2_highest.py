
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime
from math import e 
import os.path 
import sys  
import pyfolio
import backtrader as bt
import numpy as np
import warnings
import pandas as pd
warnings.filterwarnings("ignore")
# 建立一個backtrader回測框架
class Highest_high(bt.Strategy):
    #設置sma的參數，根據官方照此設置可進行暴力演算，得知何種參數最佳
    params = (
        ('highest', 6),
        ('in_amount',4),
        ('stoploss', 0.1),
        ('takeprofit', 0.2),
    )

    #這裡是log，當交易發生時呼叫log函數可以將交易print出來
    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        # print('%s, %s' % (dt.isoformat(), txt))

    #init定義你會用到的數據
    def __init__(self):
        #呼叫high序列備用
        self.datahigh = self.datas[0].high
        #呼叫close序列備用
        self.dataclose = self.datas[0].close
        #追蹤order、buyprice跟buycomm使用，可用可不用
        self.order = None
        self.buyprice = None
        self.buycomm = None
        #使用指標套件給的最高價判斷函數Highest
        self.the_highest_high = bt.ind.Highest(self.datahigh, period=self.params.highest)
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
        # 檢查有無pending的訂單
        if self.order:
            return
        #self.position.size獲得目前倉位資訊，當size<指定進場次數時則允許買入
        if self.position.size < self.params.in_amount*1000:
            #當現在的高大於前面n根的最高價時準備執行買入
            if self.datahigh > self.the_highest_high[-1]:
                # 紀錄買單提交
                self.log('BUY CREATE, %.2f' % self.dataclose[0])
                # 買進
                self.order = self.buy()    
        #當庫存部位不為0但表有庫存
        if self.position.size !=0:
            #獲取庫存成本
            costs = self.position.price
            #當收盤價大於平均成本的10%停利賣出
            if self.dataclose[0] > costs + (costs*self.params.takeprofit):
                self.close()
                self.log('Take Profit, %.2f' % self.dataclose[0])
            #當收盤價小於平均成本
            elif self.dataclose[0] < costs-(costs*self.params.stoploss):
                self.close()
                self.log('Stop Loss, %.2f' % self.dataclose[0])
        
    # #回測終止時print出結果
    # def stop(self):
    #     print(f'Fast MA: {self.params.fast_period} | Slow MA: {self.params.slow_period} | End Value: {self.broker.getvalue()}')

if __name__ == '__main__':
    # 創建框架
    cerebro = bt.Cerebro()
    # # 放入策略
    # cerebro.addstrategy(Highest_high)
    # # 放入策略
    cerebro.optstrategy(
        Highest_high,
        highest = range(5, 9), 
        in_amount = range(1, 5),
        stoploss = np.arange(0.1, 0.5, 0.1),
        takeprofit = np.arange(0.1, 0.5 ,0.1)
        )

    # 使用框架的資料取得函數
    data = bt.feeds.YahooFinanceData(
        dataname='2317.TW',
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
    
    #===================Pyfolio===================
    #cerebro.addanalyzer(bt.analyzers.PyFolio, _name='pyfolio')

    # 在設置完傭金、起始金額以及買入股數之後，我們加入三種分析
    cerebro.addanalyzer(bt.analyzers.SharpeRatio)
    cerebro.addanalyzer(bt.analyzers.Returns)
    cerebro.addanalyzer(bt.analyzers.DrawDown)
    results = cerebro.run(maxcpus=1)
    #準備list存放每一個參數及結果
    par1,par2,par3,par4,ret,down,sharpe_r = [],[],[],[],[],[],[]
    #迴圈每一個結果
    for strat in results:
        #因為結果是用list包起來(範例在下註解)，所以我們要[0]取值
        #[<backtrader.cerebro.OptReturn object at 0x0000024FF9717CC8>]
        strat = strat[0]
        #get_analysis()獲得值
        a_return = strat.analyzers.returns.get_analysis()
        drawDown = strat.analyzers.drawdown.get_analysis()
        sharpe = strat.analyzers.sharperatio.get_analysis()
        #依序裝入資料，可用strat.params.xx獲取參數
        par1.append(strat.params.highest)
        par2.append(strat.params.in_amount)
        par3.append(strat.params.stoploss)
        par4.append(strat.params.takeprofit)
        #rtot代表總回報，獲取總回報
        ret.append(a_return['rtot'])
        #我們關注最大的drawdown，因此如下取值
        down.append(drawDown['max']['drawdown'])
        #獲取sharpe ratio
        sharpe_r.append(sharpe['sharperatio'])
    #組裝成dataframe
    result_df = pd.DataFrame()
    result_df['Highest'] = par1
    result_df['in_amount'] = par2
    result_df['stoploss'] = par3
    result_df['takeprofit'] = par4
    result_df['total profit'] = ret
    result_df['Max Drawdown'] = down
    result_df['Sharpe Ratio'] = sharpe_r
    #根據總報酬來排列
    result_df = result_df.sort_values(by=['total profit'],ascending=False)
    print(result_df)
        
    #畫Kbars
    # cerebro.plot(style='candlestick', barup='red', bardown='green')

    #===================Pyfolio===================
    # strat = results[0]
    # pyfoliozer = strat.analyzers.getbyname('pyfolio')
    # returns, positions, transactions, gross_lev = pyfoliozer.get_pf_items()
  
    # # # pyfolio showtime
    # import pyfolio as pf
    # pf.create_full_tear_sheet(
    # returns,
    # positions=positions,
    # transactions=transactions,
    # live_start_date='2018-01-01')  # This date is sample specific)

