import requests
import json
import pandas as pd
def twse_data(r_date:str):
    #一樣我們對api進行請求
    data = requests.get(f'https://www.twse.com.tw/fund/T86?response=json&date={r_date}&selectType=ALLBUT0999&_=1614316365630')
    #使用json套件將他loads成json格式之後處理
    data_json = json.loads(data.text)
    #我們知道了欄位是fields，資料是data
    data_store = pd.DataFrame(data_json['data'],columns=data_json['fields'])
    return data_store


