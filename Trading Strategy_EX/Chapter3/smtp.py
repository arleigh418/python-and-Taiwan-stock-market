import sys
sys.path.append('D:\Trading Strategy_EX\Chapter3')
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
#從AES_Encrytion資料夾中import encrype_process.py裡面的所有函數*
from AES_Encryption.encrype_process import *
#節錄原先的寄信函數
def send_mail(mail_list:list, subject:str, body:str, mode :str , file_path:list, file_name:list):
    #創建一個MIMEMultipart()類
    msg = MIMEMultipart()
    user_id = 'a*********@gmail.com'
    password = '***************'
    #對它傳入三個基本信息: 寄件者(From)、收件者(To)、標題(Subject)
    msg['From'] = user_id
    #使用join將list中的元素以逗號黏起來
    msg['To'] = ",".join(mail_list)
    msg['Subject'] = subject
    #呼叫Attach，並傳入content信件內容
    if mode =='html':
        msg.attach(MIMEText(body, mode))
    else:
        msg.attach(MIMEText(body))
    #if else條件判斷使用者傳入的是否為None
    if file_path==None:
        pass
    #如果有傳入
    else:
        assert len(file_path) == len(file_name)
        for x in range(len(file_path)):
            #先透過內建的with open讀取檔案
            with open(file_path[x], 'rb') as opened:
                openedfile = opened.read()
            #呼叫MIMEApplication並放入byte類型
            attachedfile = MIMEApplication(openedfile)
            #根據指示加入至附檔，並可以指定與原本檔名不一樣的獨立檔名
            attachedfile.add_header('content-disposition', 'attachment', filename = file_name[x])
            #跟上面attach信件內容一樣，我們把附檔資訊也attach進去
            msg.attach(attachedfile)
    #設定smtp server，以gmail當例子
    server = smtplib.SMTP('smtp.gmail.com', 587)
    #TLS安全傳輸設定
    server.starttls()
    #登入你的gmail帳密
    server.login(user_id, password)
    #msg是Mimemulipart類，我們將他轉為sendmail函數才接受的字串
    text = msg.as_string()
    #指定寄件者跟收件者，還有剛剛加的信件內容、標題、附檔等等資訊(text)
    server.sendmail(user_id, mail_list , text)
    #斷線
    server.quit()

#測試加入了加解密套件的程式
#定義收件者
mail_list = ['*************.com']
#標題
subject = '測試測試'
#內容
body = '借我測試'

#要夾檔的位置
file_path = [r"D:\test.docx",r"D:\test2.docx"]
#希望傳送的檔名
file_name = ["借我測.docx","借我測2.docx"]
send_mail(mail_list, subject, body,'text', file_path, file_name)
