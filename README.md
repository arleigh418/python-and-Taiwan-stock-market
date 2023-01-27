# Python 金融市場賺大錢聖經：寫出你的專屬指標


## 重要事記
#### 快速索引
[google寄信已不支援低安全性模式](https://github.com/arleigh418/python-and-Taiwan-stock-market/blob/main/README.md#google寄信已不支援低安全性模式)

[2-3小節yahoo_price爬蟲更新](https://github.com/arleigh418/python-and-Taiwan-stock-market/blob/main/README.md#2-3小節yahoo_price爬蟲更新)

[backtrader FileNotFoundError](https://github.com/arleigh418/python-and-Taiwan-stock-market/blob/main/README.md#backtrader-filenotfounderror)

[借串宣傳線上課程>< - Python期貨程式交易課程](https://github.com/arleigh418/python-and-Taiwan-stock-market/blob/main/README.md#%E5%80%9F%E4%B8%B2%E5%AE%A3%E5%82%B3%E7%B7%9A%E4%B8%8A%E8%AA%B2%E7%A8%8B---python%E5%85%A8%E6%96%B9%E4%BD%8D%E6%9C%9F%E8%B2%A8%E8%AA%B2%E7%A8%8B---%E5%BE%9E%E5%9F%BA%E7%A4%8E%E7%88%AC%E8%9F%B2%E5%9B%9E%E6%B8%ACline%E6%8F%90%E9%86%92%E5%88%B0ai%E6%87%89%E7%94%A8)

[Yahoo股市網站更新](https://github.com/arleigh418/python-and-Taiwan-stock-market/blob/main/README.md#yahoo%E8%82%A1%E5%B8%82%E7%B6%B2%E7%AB%99%E6%9B%B4%E6%96%B0)

[新增進階補充](https://github.com/arleigh418/python-and-Taiwan-stock-market/blob/main/README.md#%E6%96%B0%E5%A2%9E%E9%80%B2%E9%9A%8E%E8%A3%9C%E5%85%85)
<br>
<br>


## google寄信已不支援低安全性模式
#### 最後更新2022/6/18

google在五月底時不支援低安全模式,因此書中介紹的寄信方式需要修改.
基本上現在要採用google的應用程式密碼功能產生出來的密碼才可做使用
步驟如下可參考：
1. 確保您的帳戶通過兩步驟驗證
2. 通過後，一樣至安全性，您應該可以如下圖看到應用程式密碼，請您利用該功能產出密碼 (要通過兩步驟驗證 才會看到應用程式密碼這個選項)
3. 將您原先程式中的密碼換成第二步驟google所產生出來的密碼應就可寄信，其他部分無需調整

您也可以參考: https://github.com/arleigh418/python-and-Taiwan-stock-market/issues/28

<br>


## 2-3小節yahoo_price爬蟲更新
#### 最後更新2023/1/27

經讀者反應，該網頁有小幅度的變更，tag變得不一樣導致爬蟲無法獲取資料。
不過變更的幅度不大，您可以先嘗試自行抓抓看新tag。
經測試以下tag目前可正常獲取資料
```
price = soup.find("fin-streamer", {"data-test": "qsp-price"})
```
<br>


## backtrader FileNotFoundError
#### 最後更新2022/1/3

backtrader的FileNotFoundError看起來是有一段小段時間都未被官方修復，因此如果您看到此Error，請首先嘗試書中4.2章節，4-48頁的backtrader的可能問題之一。

<br>


## 借串宣傳線上課程 - Python全方位期貨課程 - 從基礎、爬蟲、回測、Line提醒到AI應用
#### 最後更新2021/11/10
#### masterTalk平台線上課程 - [Python全方位期貨課程 - 從基礎、爬蟲、回測、Line提醒到AI應用](https://mastertalks.tw/products/python-futures?ref=ArleighChang)

最近有幸受邀在mastertalk上開設線上課程，對於看完本書股票應用的同學，如果對期貨這個領域有興趣，歡迎參考。
<br>

我們會將書上的部分技術如何應用在期貨上做出教學，如backtrader。並且實際的應用一些深度學習、機器學習的模型用於價格、漲跌預測。
(當然如果您只是一些期貨應用的小問題，您可以提出issue，我們可以來聊聊，或者我可以在另一篇進階補充中特別說明。此課程純推廣。)

<br>


## Yahoo股市網站更新
#### 最後更新2021/09/27
#### 新版的Yahoo新聞爬蟲請參考[yahoo_news_2.py](https://github.com/arleigh418/python-and-Taiwan-stock-market/tree/main/Trading%20Strategy_EX/Chapter2/yahoo_news_2.py)
需要特別注意，原先utility.py裡面使用的yahoo_new.py，因為已經失效，建議您將yahoo_news_2.py的函數貼utility.py後，引用yahoo_news_2來獲取新聞

Yahoo股市的網站看起來經歷了一場巨大的更新。
很可惜我三四年前爬新聞到撰寫此書時都沒有什麼會影響到程式的更新，所以我認為他算是教學的穩定標的。
不過最近有一波巨大的更新，因此2.4章節(頁數2.49)開始的爬取Yahoo新聞的環節以及3.9章節(3-148)有使用到新聞的部分失效，但我還是希望您能夠看過內容，大致了解一下舊版的網站的爬蟲過程
<br>

除網站的tag變更，風格大幅改變之外，我認為在技術上影響最大的在於原本是頁數，現在變成滾動式下拉才會有新聞出來。
如果要爬取完整新聞，在技術上來說我認為難度就提升了一個檔次，變得不太適合初學者爬蟲的標的。
因為滾動式網頁通常解法就是要用Selenium瀏覽器模擬滾動，然後邊滾邊收集新聞。
我初步測試過，這個新式網頁是可以滾到底的，滾到1個月前的新聞。
如果大家對Selenium有興趣可以在issue中提出，如果人數有個大概三四個，大約一兩周我會生出一個範例(抱歉還有正職工作要做，只能用零碎時間開發)。
<br>

不過如果是較基本的應用，倒是挺容易的。
原則上較初階的設計方式是這樣，網頁若直接爬取，大約可獲得18-21篇左右的新聞。
因此在設計上初階的方法就是我們將舊的新聞爬蟲的頁數改為想要獲得頭幾篇新聞。
例如舊的傳入2代表我想要2頁新聞，新的傳入2則代表我只看最新的兩篇新聞。
這樣的設計對初學者來說是更加友善的。
如果您要正式使用，請記得之後章節的utility.py通用那一包的Yahoo新聞的函式要記得替換。
因為設計上較為倉促，有任何bug或者是您希望有任何更活潑的設計，都歡迎提出來大家一起討論研究!感謝您的體諒!

<br>


## 新增進階補充
#### 最後更新2021/09/20
我會在另一個地方不定時的分享一些書中沒有說到，但我們有在使用的其他技術。

如果您閱讀完此書，具備一些基本的了解，可以來這裡看看。有任何問題歡迎提出issue或是透過信箱聯繫我。

https://github.com/arleigh418/python-and-Taiwan-stock-market-Advanced
<br>



## 章節對照表
<table>
    <tr>
        <td>檔案名稱</td>
        <td>對照章節</td>
    </tr>
 
 <tr>
        <td>Trading_Strategy_EX/Chapter2/stock_list.py</td>
        <td>2.2</td>
    </tr>
 
 <tr>
        <td>Trading_Strategy_EX/Chapter2/yahoo_price.py</td>
        <td>2.3</td>
    </tr>
 
 <tr>
        <td>Trading Strategy_EX/Chapter2/yahoo_news.py (因網站更新爬蟲失效) <br> Trading Strategy_EX/Chapter2/yahoo_news_2.py (因應新網站的新爬蟲)</td>
        <td>2.4</td>
    </tr>
 
 <tr>
        <td>Trading_Strategy_EX/Chapter2/TWSE.py</td>
        <td>2.5</td>
    </tr>
 
 <tr>
        <td>Trading_Strategy_EX/Chapter3/yfinance_example.py</td>
        <td>3.1</td>
    </tr>
 
 <tr>
        <td>Trading_Strategy_EX/Chapter3/pd_example.py <br> Trading_Strategy_EX/Chapter3/ta_example.py <br> Trading_Strategy_EX/Chapter3/mine_ta.py</td>
        <td>3.2</td>
    </tr>
 
 <tr>
        <td>Trading_Strategy_EX/Chapter3/generate_picture_example.py</td>
        <td>3.3</td>
    </tr>
 
 <tr>
        <td>Trading_Strategy_EX/Chapter3/smtp.py</td>
        <td>3.4</td>
    </tr>
 
 <tr>
        <td>Trading_Strategy_EX/Chapter3/smtp2.py <br> Trading_Strategy_EX/Chapter3/AES_Encryption/</td>
        <td>3.5</td>
    </tr>
 
 <tr>
        <td>Trading_Strategy_EX/Chapter3/is_open.py <br> Trading_Strategy_EX/Chapter3/deal_holiday.py </td>
        <td>3.6</td>
    </tr>
 
 <tr>
        <td>Trading/1_buy_follow_corp.py</td>
        <td>3.7</td>
    </tr>
    
 <tr>
        <td>Trading/2_buy_with_devidend.py <br> Trading/2_2_buy_with_dividend_price.py</td>
        <td>3.8</td>
    </tr>

<tr>
    <td>Trading/3_buy_with_price_fall.py</td>
    <td>3.9</td>
</tr>

<tr>
    <td>Trading/strategy_research.py</td>
    <td>4.1</td>
</tr>

<tr>
    <td>Trading/backtest_research.py</td>
    <td>4.2</td>
</tr>

<tr>
    <td>Trading/tech1_ma_strategy.py</td>
    <td>4.3</td>
</tr>

<tr>
    <td>Trading/tech2_highest.py</td>
    <td>4.4</td>
</tr>

<tr>
    <td>Trading/tech3_macd_ma.py</td>
    <td>4.5</td>
</tr>

<tr>
    <td>Trading Strategy_EX/Chapter3/holidaySchedule.csv</td>
    <td>下載下來的2021股市休市表</td>
</tr>

<tr>
    <td>Trading Strategy_EX\Chapter3\AES_Encryption <br> Trading\AES_Encryption </td>
    <td>帳密加解密工具包</td>
</tr>

<tr>
    <td>Trading\holiday.xlsx</td>
    <td>經處理過後的判斷是否開盤用</td>
</tr>

<tr>
    <td>Trading\stock_list.xlsx</td>
    <td>股票列表(請自行運行程式更新)</td>
</tr>
</table>
<br>



## 勘誤表
<table>
    <tr>
        <td>訂正日期</td>
        <td>對照章節</td>
        <td>頁數</td>
        <td>對照檔案</td>
        <td>錯誤原因</td>
        <td>修正內容</td>
        <td>勘誤發現</td>
    </tr>
 
</table>



## 購買
博客來: https://www.books.com.tw/products/0010901963?loc=M_0039_001

momo: https://m.momoshop.com.tw/goods.momo?i_code=9261467

天瓏: https://www.tenlong.com.tw/products/9789860776294

誠品: https://www.eslite.com/product/1001313432682066432001

<br>


