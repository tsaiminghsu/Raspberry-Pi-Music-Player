import os
from os.path import join
import subprocess
from time import sleep, time
import RPi.GPIO as GPIO
import numpy as np

# --- GPIO 設定 ---
input_pin = 5
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(input_pin, GPIO.IN)

# Shift Registor 設定
DS, SHCP, STCP = 6, 12, 21
GPIO.setup(DS, GPIO.OUT)
GPIO.setup(SHCP, GPIO.OUT)
GPIO.setup(STCP, GPIO.OUT)

# Keypad 設定
rows = [24, 25, 26, 20]
cols = [27, 22, 23]
keys = [
    ['1','2','3'],
    ['4','5','6'],
    ['7','8','9'],
    ['*','0','#']
]
for row_pin in rows:
    GPIO.setup(row_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
for col_pin in cols:
    GPIO.setup(col_pin, GPIO.OUT)

# 7 段顯示器設定
seg = [
    [1,0,0,0,0,0,0], # 0
    [1,1,1,1,0,0,1], # 1
    [0,1,0,0,1,0,0], # 2
    [0,1,1,0,0,0,0], # 3
    [0,0,1,1,0,0,1], # 4
    [0,0,1,0,0,1,0], # 5
    [0,0,0,0,0,1,0], # 6
    [1,1,1,1,0,0,0], # 7
    [0,0,0,0,0,0,0], # 8
    [0,0,1,0,0,0,0]  # 9
]

def clock(pin):
    GPIO.output(pin, 1)
    GPIO.output(pin, 0)

def latch(pin):
    GPIO.output(pin, 1)
    GPIO.output(pin, 0)

def display(index, dot):
    tenDigit = int(index / 10)
    unitDigit = index % 10
    if tenDigit == 0:
        digits = [[1,0,0,0,0,0,0], seg[unitDigit]]
    else:
        digits = [seg[tenDigit], seg[unitDigit]]
    clock(SHCP)
    for x in range(2):
        for bit in digits[x]:
            GPIO.output(DS, bit)
            latch(SHCP)
        GPIO.output(DS, dot)
        latch(SHCP)
    clock(STCP)

def get_key():
    key = None
    for col_num, col_pin in enumerate(cols):
        GPIO.output(col_pin, 1)
        for row_num, row_pin in enumerate(rows):
            if GPIO.input(row_pin):
                key = keys[row_num][col_num]
        GPIO.output(col_pin, 0)
    return key

# --- 主程式區 ---
key_input = ''
flag = 1
pt = 0
st = 0
player = None
prev_key = None
last_input_time = time()

while True:
    key = get_key()
    now = time()

    # 防彈跳按鍵偵測
    if key and key != prev_key and (now - last_input_time) > 0.5:
        last_input_time = now
        prev_key = key

        if key == '*':
            print(f"輸入：{key_input}")
            path = '/home/pi/Music/' + key_input
            for root, _, files in os.walk(path):
                for i in files:
                    if key_input in i:
                        f = join(root, i)
                        print("播放檔案：", f)
                        if player and player.poll() is None:
                            player.terminate()
                            player.wait()
                        player = subprocess.Popen(["omxplayer", f], stdin=subprocess.PIPE)
        elif key == '#':
            key_input = ''
        else:
            key_input += key
            try:
                display(int(key_input), 1)
            except:
                pass
            print("當前輸入：", key_input)

    elif not key:
        prev_key = None

    # 自動播放預設音樂一次
    if flag == 1:
        path = '/home/pi/Music/7th_Floor_Tango.mp3'
        if player and player.poll() is None:
            player.terminate()
            player.wait()
        player = subprocess.Popen(["omxplayer", path], stdin=subprocess.PIPE)
        flag = 0
        st = 0

    # 感應器觸發中止播放
    if GPIO.input(input_pin) == False:
        sleep(0.1)
        if player and player.poll() is None:
            player.terminate()
            player.wait()
            print("音樂播放中止 by 感應器")

    else:
        if player:
            fi = player.poll()
            if fi == 0 and st == 0:
                flag = 1
                pt += 1

    sleep(0.05)
