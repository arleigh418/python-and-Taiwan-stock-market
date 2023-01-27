#import套件
import requests
#from xxx import xxx意思是我只需要用到bs4裡面的BeautifulSoup這個Class，我就不用全部import了，我只import BeautifulSoup就好，省時省資源
from bs4 import BeautifulSoup
#定義函數名stock_price，並且需要傳入字串類型的股票代號
def stock_price(stock:str):
    #準備headers
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36"   
        }
    #使用f-string變動網址中的股價部分，而帶入的資訊就是函數所需的股票代號
    data = requests.get(f"https://finance.yahoo.com/quote/{stock}?p={stock}",headers=headers)
    #準備使用BeautifulSoup進行解析
    soup = BeautifulSoup(data.text)
    #find尋找元素
    price = soup.find("fin-streamer", {"data-test": "qsp-price"})
    #返回float的價格資訊
    return price.text
