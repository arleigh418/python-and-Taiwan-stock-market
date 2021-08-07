#import必要套件
import pandas as pd
import datetime

#讀取下載的csv檔案，skiprows可以讓你跳過第一列，或甚至多列
x = pd.read_csv("D:\Trading Strategy_EX\Chapter3\holidaySchedule.csv",encoding='big5',skiprows=[0])
#today獲取今天的日期
today = datetime.date.today()
#透過strftime只留下年
convert_today = today.strftime('%Y')
#針對日期apply，將2021加上年與原先的日期
x['日期'] = x['日期'].apply(lambda x:convert_today+'年'+x)

#一樣對日期做apply，並且replace年月為/，日為空白
x['日期'] = x['日期'].apply(lambda x:x.replace('年','/'))
x['日期'] = x['日期'].apply(lambda x:x.replace('月','/'))
x['日期'] = x['日期'].apply(lambda x:x.replace('日',''))
print(x['日期'])
#儲存成名為holiday.xlsx的檔案
x['日期'].to_excel('D:\Trading Strategy_EX\Chapter3\holiday.xlsx',columns=['日期'])