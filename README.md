# python and  Taiwan stock market 

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
        <td>Trading Strategy_EX/Chapter2/yahoo_news.py</td>
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


## 重要事記
尚無

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

## 相關技術補充區
### 相關技術補充區1 - 消息推送
關於消息推送我們是利用mail的形式，因為mail的應用比較廣，也比較正式，通常稍微大型的公司行號都比較不接受使用Line發送一些程式訊息。

但如果你想用Line發送，有個非常簡單的方式，那就是Line notify。

這篇文章寫得很清楚，推薦給大家 : https://ithelp.ithome.com.tw/articles/10234115

步驟很簡單:
1. 下載下這位大神提供的程式
2. 至Line申請token (文章有給申請網址)，然後你可以創建一個空群組，在申請Token的畫面中選擇該空群組
3. 把LINE Notify這位官方帳號邀請到你的空群組
4. 執行1.下載下來的程式即可成功推播
