#import套件，可將pandas簡寫成pd，呼叫函數pd.xxx而不需pandas.xx
import pandas as pd
import requests
#加入headers
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36"   
    }
#對網站進行requests，並加入指定的headers一同請求
html_data = requests.get("https://isin.twse.com.tw/isin/C_public.jsp?strMode=2",headers=headers)

#使用pandas的read_html處理表格式
x = pd.read_html(html_data.text)
#list取出list裡面的第一個元素，就是我們的Dataframe
x = x[0]
#pandas的好用函數iloc切片，我們指定dataframe的欄位為第一列
x.columns  = x.iloc[0,:]
#欄位雖然變成了正確的，但本來的那一列仍然存在，我們把它拿掉
x = x.iloc[1:,:]
#使用split方法，以兩個空白切割字串，並取切割完後第一個，儲存至新增的代號欄位
x['代號'] = x['有價證券代號及名稱'].apply(lambda x: x.split()[0])
#使用split方法，以兩個空白切割字串，並取切割完後第一個，儲存至新增的股票名稱欄位
x['股票名稱'] = x['有價證券代號及名稱'].apply(lambda x: x.split()[-1])
#善用to_datetime函數，並將無法轉成datetime的資料化為Nan
x['上市日'] = pd.to_datetime(x['上市日'], errors='coerce')
#把上市日的Nan去掉即可
x = x.dropna(subset=['上市日'])
#Drop掉不要的欄位
x = x.drop(['有價證券代號及名稱', '國際證券辨識號碼(ISIN Code)', 'CFICode','備註'], axis=1)
#更換剩餘的欄位順序
x = x[['代號','股票名稱', '上市日', '市場別', '產業別']]
#Drop掉產業別是空的欄位
x = x.dropna(subset=['產業別'])
#pandas的str.isdigit()函數，確認是不是為數字
x = x[x["代號"].str.isdigit()]
#印出x來看
print(x)
#儲存成excel
x.to_excel('D:\Trading Strategy_EX\Chapter2\stock_list.xlsx')
