import sys
sys.path.append('D:\Trading')
import utility_f as uf
import pandas as pd
import yfinance as yf
import numpy as np
import datetime
import traceback
try:
    #讀取高配息清單
    data = pd.read_excel('D:/Trading/dividend_list.xlsx')
    #獲取代號
    target_stock = data['代號'].tolist()
    #獲取今日日期
    today = datetime.date.today()
    #傳入判斷今天是否為營業日
    if_trade = uf.is_open(today)
    # #如果是N，表示沒開盤，準備寄信
    if if_trade=='N':
        #沒開盤應該收件者
        mail_list = ['a*****@gmail.com']
        #標題為三大法人篩選，今日休市
        subject = f'{today} 小幫手高配息低股價，每日價格比對 - 今日休市'
        #郵件內容為空
        body = ''
        #寄信
        uf.send_mail(mail_list, subject, body, 'text',None, None)
        exit()

    #獲取過去一年的日期，我們以365天估算
    date_start = today + datetime.timedelta(days =-365)
    #轉為str格式等一下準備傳入yfinance的history獲取歷史股價
    date_start = date_start.strftime('%Y-%m-%d')
    #獲取T+1日，因為yfinance的end日期是到T-1
    date_end = today + datetime.timedelta(days =1)
    #轉為str格式等一下準備傳入yfinance的history獲取歷史股價
    date_end = date_end.strftime('%Y-%m-%d')

    #創建空list備用
    target_store = []
    highest_store = []
    now_price_store = []
    #迴圈處理每一支目標股票
    for target in target_stock:
        #獲取目標股票的Ticker類
        stock = yf.Ticker(f'{target}.TW')
        #傳入start跟end獲取歷史股價
        df = stock.history(start=date_start,end=date_end) 
        #轉為array並使用np.max獲取最大值
        highest = np.max(df['High'].values)
        #取最後一筆的Close價格作為目標
        now_price =df['Close'].values[-1] 
        #如果目標小於一年內最高價的70%則執行以下操作
        if  now_price< highest*0.7:
            #儲存股票代號
            target_store.append(target)
            #儲存一年內最高價
            highest_store.append(highest)
            #儲存最近的收盤價
            now_price_store.append(now_price)
            #print出來觀賞
            print(f'Stock: {target} | high 70%: {highest*0.7} | now: {now_price} | Status : Get!')
    #讀取所有股票清單
    all_stock_list = pd.read_excel('D:/Trading/stock_list.xlsx')
    #創建空list備用
    stock_name_store = []
    #loop符合我們目標的股票
    for st in target_store:
        #dataframe的篩選，篩選出目標股票
        select_data = all_stock_list[(all_stock_list[u'代號']==st)]
        #取得後取股票平稱後轉values再取裡面的元素
        target = select_data['股票名稱'].values[0]
        #append進list
        stock_name_store.append(target)
    #創建空的dataframe準備寄信
    empty_df = pd.DataFrame()
    empty_df['日期'] = len(target_store)*[today]
    empty_df['股票代號'] = target_store
    empty_df['股票名稱'] = stock_name_store
    empty_df['最近收盤'] =  now_price_store
    empty_df['一年內最高'] = highest_store
    #將dataframe轉為html格式
    empty_df = empty_df.to_html(index=False)
    print(empty_df)
    #製作html格式
    body = f'''<html>
                <font face="微軟正黑體"></font>
                <body>
                <h4>
                小幫手系列偵測下表股票配息高且股價相對低 
                </h4>
                {empty_df}
                <h5>投資理財有賺有賠，請謹慎評估風險</h5>
                </body>
                </html>'''
    #寄信名單
    mail_list = ['a*****@gmail.com','0*****@gm.scu.edu.tw']
    #標題我們加上日期，淺顯易懂
    subject = f'{today}  小幫手高配息低股價-每日價格比對'
    #寄信
    uf.send_mail(mail_list, subject, body,'html', None, None)
except SystemExit:
    print('Its OK')
except:
    today = datetime.date.today()
    #收件名單
    mail_list = ['a*****@gmail.com','0*****@gm.scu.edu.tw']
    #標題我們加上日期，淺顯易懂
    subject = f'{today}  小幫手高配息低股價-每日價格比對異常'
    #內容就是剛剛篩選完成的股票
    body = traceback.format_exc()
    #寄信
    uf.send_mail(mail_list, subject, body,'text', None, None)