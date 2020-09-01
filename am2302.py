# -*- coding: utf-8 -*-
"""
参考:
https://www.souichi.club/raspberrypi/temperature-and-humidity02/
"""

import os

# DHT
import Adafruit_DHT
from time import sleep
from datetime import datetime

# mail
import smtplib, ssl
from email.mime.text import MIMEText


sensor = Adafruit_DHT.DHT22
pin = 4  # GPIO4

INTERVAL = 300 # 監視間隔（秒）
RETRY_TIME = 3 # dht22から値が取得できなかった時のリトライまでの秒数
MAX_RETRY = 20 # dht22から温湿度が取得できなかった時の最大リトライ回数

PLACE = 'yourplace' # 設置場所
HUM_MAX = 70.0  # 設定湿度
TEMP_MAX = 28.0 # 設定温度

GMAIL_ACCOUNT = 'frommail'
GMAIL_PASSWORD = 'password'
MAIL_TO = 'tomail'


class EnvSensorClass: # 温湿度センサークラス
    def GetTemp(self): # 温湿度を取得
        retry_count = 0
        while True: # MAX_RETRY回まで繰り返す
            retry_count += 1
            humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
            if humidity is not None and temperature is not None: # 取得できたら温度と湿度を返す
                return humidity, temperature
            elif retry_count >= MAX_RETRY:
                return 99.9, 99.9 # MAX_RETRYを過ぎても取得できなかった時に温湿度99.9を返す
            #sleep(RETRY_TIME)


def SendMail(temp, hum, detail):

    # メールデータ(MIME)の作成
    subject = 'Warning From {0}'.format(PLACE)
    msg = MIMEText(detail, "html")
    msg["Subject"] = subject
    msg["To"] = MAIL_TO
    msg["From"] = GMAIL_ACCOUNT

    # Gmailに接続
    context = ssl.create_default_context()
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=10, context=context)
    server.login(GMAIL_ACCOUNT, GMAIL_PASSWORD)
    server.send_message(msg) # メールの送信


def CreateMsg(temp, hum):

    # 現在日時
    ymdhms = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

    # ワーニングレベル
    level = "Info"
    if temp >= TEMP_MAX and hum >= HUM_MAX:
        level = "Warning-TEMP-HUM"
    elif temp >= TEMP_MAX:
        level = "Warning-TEMP"
    elif hum >= HUM_MAX:
        level = "Warning-HUM"

    # 温度と湿度
    tempstr = '{0:0.1f}'.format(temp)
    humstr = '{0:0.1f}'.format(hum)

    detail = '{0} [{1}] {2} {3}'.format(ymdhms, level, tempstr, humstr)
    return detail


try:
    if __name__ == "__main__":
        env = EnvSensorClass()
        while True:
            hum, temp = env.GetTemp() # 温湿度を取得
            detail = CreateMsg(temp, hum)

            if temp >= TEMP_MAX or hum >= HUM_MAX:
                SendMail(temp, hum, detail)
                print(detail + ' mailed')
            else:
                print(detail)

            break

            sleep(INTERVAL)

except KeyboardInterrupt:
    pass

