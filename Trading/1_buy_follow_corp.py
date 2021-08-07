import sys
sys.path.append('D:\Trading')
#import剛剛的函數包as uf
import utility_f as uf
import datetime
import os
import pandas as pd
import traceback
try:
    #獲取今日日期
    today = datetime.date.today()
    #傳入判斷今天是否為營業日
    if_trade = uf.is_open(today)
    #如果是N，表示沒開盤，準備寄信
    if if_trade=='N':
        #沒開盤應該收件者
        mail_list = ['a********@gmail.com']
        #標題為三大法人篩選，今日休市
        subject = f'{today} 小幫手三大法人篩選 - 今日休市'
        #郵件內容為空
        body = ''
        #寄信
        uf.send_mail(mail_list, subject, body, 'text' ,None, None)
        exit()
    #用control來控制獲得了幾個有開市的資料
    control = 0
    #迴圈搜索10次
    for i in range(0,10):
        #如果control比2還小(0、1、2實際上是三次)，我們就展開搜索
        if control <=2:
            #datetime.timedelta()可以對datetime類型作日期運算
            date_target = today + datetime.timedelta(days =-int(i))
            #用我們的函數is_open判斷是否開盤
            if_trade = uf.is_open(date_target)
            print(date_target)
            print(if_trade)
            #未開盤的話則continue直接進行下一批檢查
            if if_trade=='N':
                continue
            #有開盤則control要記得+1，並且進行三大法人買賣超處理
            else:
                #將日期轉為字串以便傳入twse_data()函數
                convert_today = date_target.strftime('%Y%m%d')
                #獲取三大法人買賣超日報
                data = uf.twse_data(convert_today)
                #儲存成excel
                data.to_excel(f'{convert_today}_twse.xlsx')
                #讀取時使用thousands參數讀取，處理數字問題
                data = pd.read_excel(f'{convert_today}_twse.xlsx',thousands=',')
                #刪除檔案避免檔案堆積
                os.remove(f'{convert_today}_twse.xlsx')
                #只保留三大法人買賣超股數大於0的
                d_s = data[(data[u'三大法人買賣超股數']>0)]
                #獲取前50名三大法人買超最大量的
                d_s = d_s[:50] 
                #當control ==0的時候意味著是第一次搜尋到清單，因此當主軸
                if control==0:
                    result = set(d_s[u'證券代號'].tolist())
                #如果不是的話我們用intersection函數來取交集
                else:
                    result = result.intersection(set(d_s[u'證券代號'].tolist()))
                #全部處理了control才+1，要注意位階，是在if else之外
                control+=1
        else:
            break
    #收件名單
    mail_list = ['a********@gmail.com','0********@gm.scu.edu.tw']
    #將結果用逗號黏成字串，非必要，但是我不喜歡list的中括號，看起來蠻醜的
    result  = ",".join(result)
    #標題我們加上日期，淺顯易懂
    subject = f'{today}  小幫手三大法人篩選'
    #內容就是剛剛篩選完成的股票
    body = f'目標股票 {result} 連續三日法人買超'
    #寄信
    uf.send_mail(mail_list, subject, body, 'text' ,None, None)
except SystemExit:
    print('Its OK')
except:
    #收件名單
    mail_list = ['a********@gmail.com','0********@gm.scu.edu.tw']
    #標題我們加上日期，淺顯易懂
    subject = f'{today}  小幫手三大法人篩選異常'
    #內容就是剛剛篩選完成的股票
    body = traceback.format_exc()
    #寄信
    uf.send_mail(mail_list, subject, body, 'text' ,None, None)























