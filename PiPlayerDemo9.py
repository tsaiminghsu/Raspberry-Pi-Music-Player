# piPlayer.py MP3 Player播放控制程式
import os
from os import walk
from os.path import join
import glob
import subprocess
from time import sleep
import RPi.GPIO as GPIO
import time
import numpy as np
input_pin = 16
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(input_pin, GPIO.IN)
# Setup 74HC595 Shift Registor pins
DS   = 6     # Serial Data
SHCP = 12     # Clock
STCP = 21     # Latch
GPIO.setup(DS, GPIO.OUT)
GPIO.setup(SHCP, GPIO.OUT)
GPIO.setup(STCP, GPIO.OUT)
rows= [24,25,26,20]
cols= [27,22,23]
key_input = ""
keys= [
    ['1','2','3'],
    ['4','5','6'],
    ['7','8','9'],
    ['*','0','#']]
# Setup 7 segment display ,Q7 ~ Q1
seg = [#[0,0,0,0,0,0,1],#0
       [1,0,0,0,0,0,0],#0
       #[1,0,0,1,1,1,1],#1
       [1,1,1,1,0,0,1],#1
       #[0,0,1,0,0,1,0],#2
       [0,1,0,0,1,0,0],#2
       #[0,0,0,0,1,1,0],#3
       [0,1,1,0,0,0,0],#3
       #[1,0,0,1,1,0,0],#4
       [0,0,1,1,0,0,1],#4
       #[0,1,0,0,1,0,0],#5
       [0,0,1,0,0,1,0],#5
       #[0,1,0,0,0,0,0],#6
       [0,0,0,0,0,1,0],#6
       #[0,0,0,1,1,1,1],#7
       [1,1,1,1,0,0,0],#7
       #[0,0,0,0,0,0,0],#8
       [0,0,0,0,0,0,0],#8
       #[0,0,0,0,1,0,0] #9
       [0,0,1,0,0,0,0]
       ]
# Send Clock signal
def clock(pin):
    GPIO.output(pin, 1)
    GPIO.output(pin, 0)
# Send Latch signal
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
    # Send signal to 74HC595 and drive two 7 segment display
    clock(SHCP)
    for x in range(2):
        for bit in digits[x]:
            GPIO.output(DS, bit)
            latch(SHCP)
        GPIO.output(DS, dot)
        latch(SHCP)
    clock(STCP)
for row_pin in rows:
    GPIO.setup(row_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
for col_pin in cols:
    GPIO.setup(col_pin, GPIO.OUT)
def get_key():
    key = np.array([0])
    for col_num, col_pin in enumerate(cols):
        GPIO.output(col_pin, 1)
        for row_num, row_pin in enumerate(rows):
            if GPIO.input(row_pin):
               key = keys[row_num][col_num]
        GPIO.output(col_pin, 0)
    return key
flag=1
pt=0
st=0
while True:
        key = get_key()
        sleep(0.1)
        if key:
              if key=='*':
                #display(0,1)
                print(key_input)
                path = '/home/pi/Music/' + key_input
                for root, dirnames, files in os.walk(path):
                    for i in files:
                      Fullpath = join(root,i)
                      FileName = join(i)
                      if key_input in FileName:
                        if key_input.startswith(key_input):
                          f = os.path.join(root, FileName)
                          print (f)
                          if f == False:
                            f=''
                            key_input=''
                          else:
                            player = subprocess.Popen(["omxplayer",f],stdin=subprocess.PIPE)
                            fi = player.poll()
                            key_input = ''
              elif key=='#':
                key_input = ''
                display(0,1)
              else:
                  if len(key_input)<=2:
                      key_input += key
                  if len(key_input)>2:
                      key_input=''
                      display(0,1)
                  else:
                      display(int(key_input),1)
                  print(key_input)
        if flag==1:
          key_input = ''
          display(0,1)
          path = '/home/pi/Music/7th_Floor_Tango.mp3'
          #player = subprocess.Popen(["omxplayer",f[pt]],stdin=subprocess.PIPE) 
          player = subprocess.Popen(["omxplayer",path],stdin=subprocess.PIPE) 
          fi = player.poll()
          flag=0
          st=0
        if GPIO.input(input_pin)==False:
          #fi = player.poll()
          #if fi!=0:
            sleep(0.1)
            os.system("killall omxplayer.bin")
            print "start"
            #time.sleep(20)
            #break
            #st=1
        else:
          #fi = player.poll()
          if (fi==0 and st==0):
              flag=1
        sleep(0.1)
