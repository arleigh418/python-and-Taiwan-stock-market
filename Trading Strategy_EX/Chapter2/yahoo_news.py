import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_yahoo_news(stock:str,target_page:int):
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
    print(x)
    import time
    for i in range(1,x+1):
        time.sleep(1)
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
    #返回dataframe
    return result

