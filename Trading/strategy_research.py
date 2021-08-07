#%%
#import需要的套件
import pyfolio as pf
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
stock = yf.Ticker(f'2330.TW')
return_ser = stock.history(start='2012-01-01',end='2021-05-16')
pf.create_returns_tear_sheet(return_ser['Close'].pct_change())




    


# %%
