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


sensor = Adafruit_DHT.DHT22
pin = 4  # GPIO4

RETRY_TIME = 3 # dht22から値が取得できなかった時のリトライまでの秒数
MAX_RETRY = 20 # dht22から温湿度が取得できなかった時の最大リトライ回数

PLACE = 'yourplace' # 設置場所
HUM_MAX = 70.0  # 設定湿度
TEMP_MAX = 28.0 # 設定温度


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

    detail = '{0} [{1}] {2:0.1f} {3:0.1f}'.format(ymdhms, level, temp, hum)
    return detail


try:
    if __name__ == "__main__":
        env = EnvSensorClass()
        hum, temp = env.GetTemp() # 温湿度を取得
        detail = CreateMsg(temp, hum)
        print(detail)

except KeyboardInterrupt:
    pass

