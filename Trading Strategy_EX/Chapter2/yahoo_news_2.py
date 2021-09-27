import requests
from bs4 import BeautifulSoup
import pandas as pd
import requests
from bs4 import BeautifulSoup
import pandas as pd

'''
設計上是先在新聞列表中取得每一篇新聞的連結，再去每一篇新聞獲取標題以及日期資訊
其實新聞列表就已經具有標題以及連結這些元素，但問題是他的時間是例如1小時前、50分鐘前、三天前
這並不是我們想要的格式，所以我們還需要一個步驟，獲取每個詳細新聞網址去裡頭獲取詳細的年月日時間(例如2021/9/27)
當然如果你不介意例如1小時前這樣的時間，那爬蟲速度應該至少可以快50%以上
因為就不需要每一篇新聞都還要為了時間資訊去request獲取資訊
看個人取捨設計了，我先寫比較繁複的，這樣你要改成簡單的也比較容易
'''

def get_yahoo_news2(stock:str,target_page:int):
    #準備headers
    headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36"   
            }
    #requests指定網址，並且帶入headers
    data = requests.get(f"https://tw.stock.yahoo.com/quote/{str(stock)}/news",headers=headers)
    #使用BeautifulSoup解析，指定解析方法html.parser可以避免warning
    soup = BeautifulSoup(data.text, "html.parser")

    #選取標題的tag來使用，讀者自行練習的時候應該會發現有許多tag可以使用，基本上可以使用就可以，未必要跟我的一樣
    all_news = soup.find_all('h3',{'class':'Mt(0) Mb(8px)'})

    #創建空list儲存每一篇新聞的連結
    all_news_store = []
    #loop每一個抓回來的元素
    for a in all_news:
        #藉由find獲得的物件還可以再find，因此我們find a元素，並且取得裡面的href，也就是網址
        news_path = a.find('a')['href'] 
        #雅虎新聞目前的設計是中間會夾雜一兩篇廣告，這些廣告的特點是他們的連結最後沒有html的文字，因此可以用這個方法剔除他們
        if news_path[-4:]=='html':
            #最後append進list備用
            all_news_store.append(news_path)

    #開始進行獲取日期，標題我也在這裡做，當然如果你要再上一個步驟就獲取標題也可以
    #創建空list備用
    date_store,title_store = [],[]
    #loop剛剛獲得的每一篇新聞網址
    for new in all_news_store:
        #做requests
        each_data = requests.get(f"{new}",headers=headers)
        #BeautifulSoup整理格式，指定解析方法html.parser可以避免warning
        each_soup = BeautifulSoup(each_data.text, "html.parser")
        #find獲取title
        title = each_soup.find('h1',{'data-test-locator':'headline'})
        #find獲取時間
        news_time = each_soup.find('div',{'class':'caas-attr-time-style'})
        #整理時間格式，只想要前面的年月日資訊，中間有空白剛好可以利用split切割空白，取第一個元素
        news_time = news_time.text.split(' ')[0]
        #這裡看個人要不要做，我不喜歡例如2021年9月27日這樣的格式，因此我用replace轉換成2021/9/27
        news_time = news_time.replace('年','/')
        news_time = news_time.replace('月','/')
        news_time = news_time.replace('日','')
        #append整理資料
        title_store.append(title.text)
        date_store.append(news_time)
    #整理成DataFrame
    result = pd.DataFrame()
    result['title'] = title_store
    result['url'] = all_news_store
    result['date'] = date_store
    #return的時候回傳使用者指定的篇數
    return result[0:target_page]

