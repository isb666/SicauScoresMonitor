
import requests
from bs4 import BeautifulSoup
import smtplib
import re
# 从email.mime.multipart中导入MIMEMultipart类
from email.mime.multipart import MIMEMultipart
# 从email.header中导入Header类
from email.header import Header

# 从email.mime.text中导入MIMEText类
from email.mime.text import MIMEText

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "zh-CN,zh;q=0.9",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "priority": "u=0, i",
    "sec-ch-ua": "\"Chromium\";v=\"124\", \"Google Chrome\";v=\"124\", \"Not-A.Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}
cookies = {
   #你的cookies
}
url = "https://jiaowu.sicau.edu.cn/xuesheng/chengji/chengji/sear_ch_all.asp"
resp = requests.get(url, headers=headers, cookies=cookies)
resp.encoding ='gbk'
datas =BeautifulSoup(resp.text.split('\n')[-1],'lxml').find_all('tr')[5:][:-2]

with open ("C:\\Users\HW\Desktop\q1.txt",'r') as fp:
    currrent_length = int(fp.read())
if len(datas)>currrent_length:
    with open("C:\\Users\HW\Desktop\q1.txt", 'w') as fp:
        fp.write(str(len(datas)))
    mes = ''
    for data in datas:
        data = [re.sub(r'\s+', '', item) for item in re.findall('>([^>]+)</td',str(data))]
        mes += f'{data[3]}\t{data[9]}分\t绩点:{data[10]}\n'

    # 1、连接邮箱服务器
    # 连接邮箱服务器：连接邮箱服务器：使用smtplib模块的类SMTP_SSL，创建一个实例对象qqMail
    qqMail = smtplib.SMTP_SSL("smtp.qq.com", 465)

    # 2、登陆邮箱
    # 设置登录邮箱的帐号为："zhangxiaofan@qq.com"，赋值给mailUser
    mailUser = "yourRobot@qq.com"
    # 将邮箱授权码"xxxxx"，赋值给mailPass
    mailPass = "xxxxxx"
    # 登录邮箱：调用对象qqMail的login()方法，传入邮箱账号和授权码
    qqMail.login(mailUser, mailPass)

    # 3、编辑收发件人
    # 设置发件人和收件人
    sender = "yourRobot@qq.com"
    receiver = "yourRealMail@qq.com"
    # 使用类MIMEMultipart，创建一个实例对象message
    message = MIMEMultipart()
    # 将主题写入 message["Subject"]
    message["Subject"] = Header("成绩更新")
    # 将发件人信息写入 message["From"]
    message["From"] = Header(f"Robot <{sender}>")
    # 将收件人信息写入 message["To"]
    message["To"] = Header(f"aaa <{receiver}>")

    # 4、构建正文
    # 设置邮件的内容，赋值给变量textContent
    textContent = mes
    # 编辑邮件正文：使用类MIMEText，创建一个实例对象mailContent
    mailContent = MIMEText(textContent, "plain", "utf8")
    message.attach(mailContent)
    # 6、发送邮件
    # 发送邮件：使用对象qqMail的sendmail方法发送邮件
    qqMail.sendmail(sender, receiver, message.as_string())
    # 输出"发送成功"
    print("发送成功")

