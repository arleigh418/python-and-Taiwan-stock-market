import pandas as pd

def mine_add_all_features(df:pd.DataFrame):
    #rolling以6為單位位移並取最大值
    Highest_high =df['High'].rolling(6).max()
    #rolling以6為單位位移並取最小值
    Lowest_low = df['Low'].rolling(6).min()
    #一樣用6根作為rolling，並且設計計算函數第一個值減去最後一個值
    O_C_high = df['High'].rolling(6).apply(lambda x : x[0]-x[-1])
    #加入dataframe
    df['OCHIGH'] = O_C_high
    df['Highest_high'] = Highest_high
    df['Lowest_Low'] = Lowest_low
    return df