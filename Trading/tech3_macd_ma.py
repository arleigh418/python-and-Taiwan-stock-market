#%%
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])

# Import the backtrader platform
import backtrader as bt
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import numpy as np
import os

class MACD_Sta(bt.Strategy):
    params = (
        ('period_me1', 12), 
        ('period_me2', 26), 
        ('period_signal', 9),
        ('period_sma1', 5),
        ('period_sma2', 20),
        ('period_sma3', 60),
        ('stoploss',0.3),
        ('takeprofit',0.1),
        )

    def __init__(self):
        #定義基本的東西
        self.order = None
        self.buyprice = None
        self.buycomm = None
        self.dataclose = self.datas[0].close
        self.datahigh = self.datas[0].high
        self.dataopen = self.datas[0].open
        #獲取快線與慢線的差值histo
        self.histogram= bt.ind.MACDHisto(period_me1=12,period_me2= 26,period_signal=9)
        #呼叫histo
        self.histo  = self.histogram.histo
        #加入三個ma
        self.sma1 = bt.indicators.SimpleMovingAverage(
            self.datas[0].close, period=self.params.period_sma1)
       
        self.sma2 = bt.indicators.SimpleMovingAverage(
            self.datas[0].close, period=self.params.period_sma2)
        self.sma3 = bt.indicators.SimpleMovingAverage(
            self.datas[0].close, period=self.params.period_sma3)
        

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))
    #策略的核心
    def next(self):
        #print出收盤價的部分
        # self.log('Close, %.2f' % self.dataclose[0])
        #檢查是否有訂單卡住，為官方示範的範例
        if self.order:
            return
        #當庫存為0
        if self.position.size==0:
            #條件一，當5ma、20ma、60ma三條線齊揚
            buy_condition1 = self.sma1[0]>self.sma1[-1] and self.sma2[0]>self.sma2[-1] and self.sma3[0]>self.sma3[-1]
            #條件二，當macd的柱狀圖有負轉正
            buy_condition2 =self.histo[-2]<0  and self.histo[-1]<0 and self.histo[0]>=0
            #同時符合兩者則進場買入
            if buy_condition1 and buy_condition2:
                #買入log
                self.log('BUY CREATE, %.2f' % self.dataclose[0])
                #買入動作
                self.order = self.buy()
        #反之有庫存則判斷是否有賣出機會
        else:
            #條件一，當前(n)小於昨日(n-1)高，但n-1高大於n-2高且n-2大於n-3
            sell_condition1 = self.datahigh[0] < self.datahigh[-1] and self.datahigh[-1] > self.datahigh[-2] and  self.datahigh[-2]>self.datahigh[-3]
            #條件二，當出現紅紅綠的線形
            sell_condition2 = self.dataopen[0] >self.dataclose[0] and self.dataclose[-1] > self.dataopen[-1] and self.dataclose[-2] > self.dataopen[-2] 
            #條件三，當收盤價至少比成本價高
            sell_condition3 = self.dataclose[0] > self.position.price*(1+self.params.takeprofit)
            #條件四，當收盤價至少比成本價低stoploss，視為停損
            sell_condition4  = self.dataclose[0] < self.position.price*(1-self.params.stoploss)
            #將條件1、2、3組合再一起
            if (sell_condition1 and sell_condition2 and sell_condition3):
                #賣出log，改為sell profit
                self.log('SELL Profit, %.2f' % self.dataclose[0])
                #平倉賣出
                self.order = self.close()
            #條件4為停損特別拉出
            elif sell_condition4:
                #賣出log，改為sell loss
                self.log('Stop Loss CREATE, %.2f' % self.dataclose[0])
                #停損賣出
                self.order = self.close()
#準備開始設置框加
if __name__ == '__main__':
    #列出目標股票
    stock_list = ['2317.TW']
    #空list備用
    final_list = []
    #迴圈目標股票
    for stock in stock_list:
        #基本的框架設置
        cerebro = bt.Cerebro()
        cerebro.addstrategy(MACD_Sta)
        #使用yfinance先獲取資料
        yf_data = yf.Ticker(stock)
        yf_data = yf_data.history(start='2018-01-01', end='2020-12-31')
        #計算期間內最高的股價，乘以1.5作為基本資金
        set_cash = np.max(yf_data['High'].values)*1.5*1000
        #pandasData讀取自備資料
        data = bt.feeds.PandasData(dataname=yf_data)
        #加入資料、設置初始資金、設置每次買入股數、設置傭金
        cerebro.adddata(data)
        cerebro.broker.setcash(set_cash)
        cerebro.addsizer(bt.sizers.FixedSize, stake=1000)
        cerebro.broker.setcommission(commission=0.0015)

        #設置三種分析
        cerebro.addanalyzer(bt.analyzers.SharpeRatio)
        cerebro.addanalyzer(bt.analyzers.Returns)
        cerebro.addanalyzer(bt.analyzers.DrawDown)
        #運行
        results = cerebro.run()
        #獲取三種分析的值
        a_return = results[0].analyzers.returns.get_analysis()
        drawDown = results[0].analyzers.drawdown.get_analysis()
        sharpe = results[0].analyzers.sharperatio.get_analysis()
  
        #將資料放入同一個list中
        con_data = [stock, set_cash, cerebro.broker.getvalue(), cerebro.broker.getvalue()-set_cash, a_return['rtot'], drawDown['max']['drawdown'], sharpe['sharperatio']]
        #append到一開始新增的list
        final_list.append(con_data)
        #plot出來
        figure = cerebro.plot(style='candlestick', barup='red', bardown='green',volume=False)
        #儲存相片
        figure[0][0].savefig(f'png/result_{stock}.png')
        #關閉相片
        plt.close()
    #產製檔案
    col = ['股票代號','投入金額','結束金額','報酬($)','總報酬(%)','MDD','Sharpe Ratio']
    final_pd = pd.DataFrame(final_list,columns=col)
    final_pd.to_excel('result.xlsx')
