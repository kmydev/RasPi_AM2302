# -*- coding: utf-8 -*-
# send a daily report mail

import os
from datetime import datetime

# mail
import smtplib, ssl
from email.mime.text import MIMEText


PLACE = 'yourplace' # 設置場所

GMAIL_ACCOUNT = 'yourmail'
GMAIL_PASSWORD = 'password'
MAIL_TO = 'tomail'

LOGDIR = '/home/pi/SensorScripts/Log/'


def SendMail(detail):

    # メールデータ(MIME)の作成
    subject = 'Daily Mail From {0}'.format(PLACE)
    msg = MIMEText(detail, "html")
    msg["Subject"] = subject
    msg["To"] = MAIL_TO
    msg["From"] = GMAIL_ACCOUNT

    # Gmailに接続
    context = ssl.create_default_context()
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=10, context=context)
    server.login(GMAIL_ACCOUNT, GMAIL_PASSWORD)
    server.send_message(msg) # メールの送信


def CreateMsg():

    detail = ''

    # 現在日時
    ymdhms = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

    # 対象ログファイル名
    logfile = '{0}{1}.log'.format(LOGDIR, datetime.now().strftime("%Y%m%d"))

    # ファイルオープン～Warning検索
    f = open(logfile, 'r')
    for s in f:
        if 'Warn' in s:
            detail += '{0}<br>'.format(s.strip())

    if len(detail) == 0:
        detail = 'no warnings today<br>'

    detail = '**** Daily Mail from {0} ****<br>{1}<br>{2}'.format(PLACE, ymdhms, detail)

    return detail


try:
    if __name__ == "__main__":
        detail = CreateMsg()
        print(detail)

        SendMail(detail)


except KeyboardInterrupt:
    pass

