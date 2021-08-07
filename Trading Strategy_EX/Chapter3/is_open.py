import pandas as pd
import datetime

def is_open(target_date:datetime.date):
    #讀取剛剛的休市日期檔案
    hd = pd.read_excel(r"D:\Trading Strategy_EX\Chapter3\holiday.xlsx")
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
    return 'Y'


