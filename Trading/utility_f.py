import requests
import json
import pandas as pd
import sys
sys.path.append('D:\Trading')
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from AES_Encryption.encrype_process import *
import pandas as pd
import datetime
from bs4 import BeautifulSoup

#是否開盤用函數，返回字串Y、N，Y代表有開盤，N反之
'''
target_date = 傳入datetime格式日期，為需要判定是否開盤的日期
'''
def is_open(target_date:datetime.date):
    #讀取剛剛的休市日期檔案
    hd = pd.read_excel(r"holiday.xlsx")
    #轉換為list備用
    hd_date = pd.to_datetime(hd['日期']).tolist()
    #將日期進行格式化
    str_date = target_date.strftime('%Y%m%d')
    #將原先是today的地方換掉
    day = target_date.weekday()
    #判定是不是星期六或日，如果是的話就print N出來
    if day == 5 or day==6:
        return 'N'
    #Loop國定假日的list
    for i in hd_date:
        #將Timestamp類格式化為與目標日期同樣的字串
        i = i.strftime('%Y%m%d')
        #檢查是否有國定假日跟目標日期一樣，如果一樣print N，表示目標日期為國定假日，結束程式
        if (i==str_date):
            return 'N'
        #Y代表不符合六日也非國定假日，有開盤返回Y
    return 'Y'

#三大法人買賣超日報，返回一份dataframe
'''
r_date = 字串格式日期，為需要查詢三大法人買賣超日報的目標日期
'''
def twse_data(r_date:str):
    #一樣我們對api進行請求
    data = requests.get(f'https://www.twse.com.tw/fund/T86?response=json&date={r_date}&selectType=ALLBUT0999&_=1614316365630')
    #使用json套件將他loads成json格式之後處理
    data_json = json.loads(data.text)
    #我們知道了欄位是fields，資料是data
    data_store = pd.DataFrame(data_json['data'],columns=data_json['fields'])
    return data_store

#寄信函數
'''
mail_list = 列表，需要寄信的清單
subject = 字串，標題
body = 字串，內容
mode = 字串，支援text跟html兩種寄信模式
file_path = 列表，想要寄出的檔案的位置
file_name = 列表，希望收件者看到的檔名
'''
def send_mail(mail_list:list, subject:str, body:str, mode :str , file_path:list, file_name:list):
    #決定金鑰跟config檔位置
    key_path = 'D:/key/'
    config_path = 'D:/config/'
    #引用加解密的主要程式check_encrype
    user_id, password = check_encrype('gmail',key_path,config_path)
    #創建一個MIMEMultipart()類
    msg = MIMEMultipart()
    #對它傳入三個基本信息: 寄件者(From)、收件者(To)、標題(Subject)
    msg['From'] = user_id
    #使用join將list中的元素以逗號黏起來
    msg['To'] = ",".join(mail_list)
    msg['Subject'] = subject
    #呼叫Attach，並傳入content信件內容
    if mode =='html':
        msg.attach(MIMEText(body, mode))
    else:
        msg.attach(MIMEText(body))
    #if else條件判斷使用者傳入的是否為None
    if file_path==None:
        pass
    #如果有傳入
    else:
        for x in range(len(file_path)):
            #先透過內建的with open讀取檔案
            with open(file_path[x], 'rb') as opened:
                openedfile = opened.read()
            #呼叫MIMEApplication並放入byte類型
            attachedfile = MIMEApplication(openedfile)
            #根據指示加入至附檔，並可以指定與原本檔名不一樣的獨立檔名
            attachedfile.add_header('content-disposition', 'attachment', filename = file_name[x])
            #跟上面attach信件內容一樣，我們把附檔資訊也attach進去
            msg.attach(attachedfile)
    #設定smtp server，以gmail當例子
    server = smtplib.SMTP('smtp.gmail.com', 587)
    #TLS安全傳輸設定
    server.starttls()
    #登入你的gmail帳密
    server.login(user_id, password)
    #msg是Mimemulipart類，我們將他轉為sendmail函數才接受的字串
    text = msg.as_string()
    #指定寄件者跟收件者，還有剛剛加的信件內容、標題、附檔等等資訊(text)
    server.sendmail(user_id, mail_list , text)
    #斷線
    server.quit()

#取得目表股票新聞函數
'''
stock = 字串，目標股票
target_page = 整數，要抓取的頁數
'''
def get_yahoo_news(stock:str,target_page:int):
    try:
        #===========================獲取頁數===========================
        #準備headers
        headers = {
                "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36"   
                }
        #requests指定網址，並且帶入headers
        data = requests.get(f"https://tw.stock.yahoo.com/q/h?s={stock}",headers=headers)
        #使用BeautifulSoup解析
        soup = BeautifulSoup(data.text)
        #find我們找到的共幾頁元素
        page = soup.find('span',{'class':'mtext'})
        #建立一個空字串
        x = ''
        #迴圈處理page這個元素，符合的就加起來
        for i in page.text:
            if i.isdigit():
                x+=i
        x = int(x)
        #如果目標頁數比x小，那我們的拿來帶入頁數的x就可以直接替換成目標頁數
        if target_page<x:
            x = target_page
    #===========================取得資料===========================
        #準備儲存變數的list
        title,url,date_store = [],[],[]
        #準備儲存所有資料的空dataframe
        result = pd.DataFrame()
        #range函數，顧名思義就是從1數到目標
        for i in range(1,x+1):
            data = requests.get(f"https://tw.stock.yahoo.com/q/h?s={stock}&pg={str(i)}",headers=headers)
            soup = BeautifulSoup(data.text)
            #find_all獲取所有都是td且屬性為height:37的tag
            article = soup.find_all('td',{'height':'37'})
            #一樣用BeautifulSoup物件來尋找定位，獲取td tag且屬性為height:29
            date_data = soup.find_all('td',{'height':'29'}) 
            #zip方法可以把多個list拿來一起loop
            for x,y in zip(article,date_data):
                #把三個資訊都append到list中
                title.append(x.text)
                url.append('https://tw.stock.yahoo.com'+x.find('a')['href'])
                date_store.append((y.text.split()[0])[1:])
        #最後用dataframe儲存起來
        result['title'] = title
        result['url'] = url
        result['date'] = date_store
    except:
        result = pd.DataFrame()
        result['title'] = ['Error']
        result['url'] = ['Error']
        result['date'] = ['Error']
    return result