# -*- coding: utf-8 -*-

import smtplib, ssl
from email.mime.text import MIMEText

# 以下にGmailの設定を書き込む
gmail_account = "yourmail"
gmail_password = "password"
# メールの送信先 --- (*2)
mail_to = "tomail"

# メールデータ(MIME)の作成 --- (*3)
subject = "メール送信テスト"
body = "メール送信テスト"
msg = MIMEText(body, "html")
msg["Subject"] = subject
msg["To"] = mail_to
msg["From"] = gmail_account

# Gmailに接続 --- (*4)
context = ssl.create_default_context()
server = smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=10, context=context)
server.login(gmail_account, gmail_password)
server.send_message(msg) # メールの送信
print("ok.")

