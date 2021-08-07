import sys
sys.path.append('D:\Trading')
import utility_f as uf
import pandas as pd
import yfinance as yf
import numpy as np
import datetime
import time
import traceback
try:
    #讀取股票清單
    data = pd.read_excel('D:/Trading/stock_list.xlsx')
    #獲取代號
    target_stock = data['代號'].tolist()
    #獲取今日日期
    today = datetime.date.today()
    #傳入判斷今天是否為營業日
    if_trade = uf.is_open(today)
    #如果是N，表示沒開盤，準備寄信
    if if_trade=='N':
        #沒開盤應該收件者
        mail_list = ['a*****@gmail.com']
        #標題為三大法人篩選，今日休市
        subject = f'{today} 小幫手暴跌中的股票偵測 - 今日休市'
        #郵件內容為空
        body = ''
        #寄信
        uf.send_mail(mail_list, subject, body, 'text',None, None)
        exit()
    #獲取過去10天的收盤價
    date_start = today + datetime.timedelta(days =-20)
    #轉為str格式等一下準備傳入yfinance的history獲取歷史股價
    date_start = date_start.strftime('%Y-%m-%d')
    #獲取T+1日，因為yfinance的end日期是到T-1
    date_end = today + datetime.timedelta(days =1)
    #轉為str格式等一下準備傳入yfinance的history獲取歷史股價
    date_end = date_end.strftime('%Y-%m-%d')
    #創建空list備用
    stock_store = []
    today_store = []
    today_fall = []
    count = 0
    #迴圈處理每一支目標股票
    for target in target_stock:
        count+=1
        time.sleep(1)
        #獲取目標股票的Ticker類
        stock = yf.Ticker(f'{target}.TW')
        #傳入start跟end獲取歷史股價
        df = stock.history(start=date_start,end=date_end) 
        #做一點基本的檢核，防止資料回傳0筆或1筆
        if len(df) >=5:
            #將收盤轉為array並且取最後一筆，今天的收盤
            today_price = df['Close'].values[-1]
            #將收盤轉為array並且取倒數第二筆，昨天的收盤
            yes_price = df['Close'].values[-2]
            #將收盤轉為array並且取倒數第二筆，前天的收盤
            be_yes_price = df['Close'].values[-3]
            #根據公式取得今日的漲跌幅
            fall_today = ((today_price - yes_price)/yes_price)*100
            #根據公式取得昨日的漲跌幅
            fall_yes = ((yes_price-be_yes_price)/be_yes_price)*100
            #兩個漲跌幅皆小於-5則是我們的目標，儲存起來。
            if fall_today<=-5 and fall_yes<=-5:
                print(f'Stock: { target} | fall today: {fall_today} | today: {today_price} | yes: {yes_price}')
                today_store.append(today_price)
                today_fall.append(fall_today)
                stock_store.append(target)
            #print出處理進度
            print(f'Dealing Stock: {target} | All Stock: {len(target_stock)} | Now: {count}')
    #控制用
    print('Get it:',stock_store)
    main_df = pd.DataFrame()
    #Loop剛剛篩選的結果
    for t in stock_store:
        #使用到跟requests有關的東西，習慣先sleep一下
        time.sleep(1)
        #我們要將目標股票的新聞連接再一起，contorl=0代表第一次loop
        #使用新聞函數獲取新聞，並且先獲取主要的dataframe，其他股票的就連接在後面
        merge_df = uf.get_yahoo_news(t,1)
        #多一個欄位叫做stock儲存這篇新聞是屬於那一支股票
        merge_df['stock'] = len(merge_df)*[t]
        main_df = main_df.append(merge_df)
    #處理要寄信的部分，首先將剛剛的新聞列表儲存成excel保存
    main_df.to_excel(f'D:/Trading/fall_stock_news.xlsx',index=False)
    #處理要寄信的部分，這裡處理我希望放在信件body的暴跌中的股票清單
    empty_dataframe = pd.DataFrame()
    empty_dataframe['股票代號'] = stock_store
    empty_dataframe['今價'] = today_store
    empty_dataframe['今日跌幅%'] = today_fall
    #希望寄出的是表格，因此我們將他轉為html備用
    empty_dataframe = empty_dataframe.to_html(index=False)
    #製作html格式
    body = f'''<html>
                <font face="微軟正黑體"></font>
                <body>
                <h4>
                小幫手系列偵測下表股票為暴跌中股票 
                </h4>
                {empty_dataframe}
                <h5>投資理財有賺有賠，請謹慎評估風險</h5>
                </body>
                </html>'''
    #寄信名單
    mail_list = ['a******@gmail.com','0******@gm.scu.edu.tw']
    #標題我們加上日期，淺顯易懂
    subject = f'{today}  小幫手暴跌中股票偵測'
    #寄信
    uf.send_mail(mail_list, subject, body,'html', [f'D:/Trading/fall_stock_news.xlsx'], ['相關新聞表.xlsx'])
except SystemExit:
    print('Its OK')
except:
    today = datetime.date.today()
    #收件名單
    mail_list = ['a******@gmail.com','0******@gm.scu.edu.tw']
    #標題我們加上日期，淺顯易懂
    subject = f'{today}  小幫手暴跌中股票異常'
    #內容就是剛剛篩選完成的股票
    body = traceback.format_exc()
    #寄信
    uf.send_mail(mail_list, subject, body,'text', None, None)