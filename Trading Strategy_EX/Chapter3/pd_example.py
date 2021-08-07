import pandas as pd
import yfinance as yf
#yfinance產出台積電股價資料
stock = yf.Ticker('2330.TW')
#獲取20170101-20210202
df = stock.history(start="2017-01-01",end="2021-02-02") 
#rolling以6為單位位移並取最大值
Highest_high =df['High'].rolling(6).max()
#rolling以6為單位位移並取最小值
Lowest_low = df['Low'].rolling(6).min()

#一樣用6根作為rolling，並且設計計算函數第一個值減去最後一個值
O_C_high = df['High'].rolling(6).apply(lambda x : x[0]-x[-1])
#加入dataframe
df['OCHIGH'] = O_C_high
#存成Excel來看一下結果
df.to_excel(r'D:\Trading Strategy_EX\Chapter3\final.xlsx')

df['Highest_high'] = Highest_high
df['Lowest_Low'] = Lowest_low
df['OCHIGH'] = O_C_high
print(df)
