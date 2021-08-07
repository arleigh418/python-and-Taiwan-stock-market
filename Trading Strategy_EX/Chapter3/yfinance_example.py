import yfinance as yf
#指定2330.TW這支股票
stock = yf.Ticker('2330.TW')
print('======獲取歷史股價-指定區間======')
df = stock.history(start="2017-01-01",end="2021-02-02") #period=max
print(df)
print('======獲取歷史股價-所有區間======')
df = stock.history(period='max') 
print(df)


print('======股票基本信息======')
df_info = stock.info
print(df_info)
print('======主要持有人======')
major_holders = stock.major_holders
print(major_holders)

print('======主要持有之機構法人======')
ins_holders =stock.institutional_holders 
print(ins_holders)

print('======取得損益表，執行看看結果======')
fin_data = stock.financials
print(fin_data)

print('======取得資產負債表，執行看看結果======')
balance_data = stock.balance_sheet
print(balance_data)

print('======取得現金流量表，執行看看結果======')
cf_data = stock.cashflow
print(cf_data)

print('======分析師建議======')
print(stock.recommendations)