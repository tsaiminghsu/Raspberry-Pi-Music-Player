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
input_pin = 5
GPIO.setmode(GPIO.BCM)
GPIO.setup(input_pin, GPIO.IN)
rows= [24,25,26,20]
cols= [27,22,23]
key_input = ""
keys= [
    ['1','2','3'],
    ['4','5','6'],
    ['7','8','9'],
    ['*','0','#']]
 
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
path = '/home/pi/Music/'
f = [os.path.join(dirpath, fn)
    for dirpath, dirnames, files in os.walk(path)
    for fn in files if fn.endswith('.mp3')]

#print f
h = len(f)
flag=1
pt=0
st=0

while True:
        key = get_key()
        sleep(0.1)
        if key:
              if key=='*':
                print(key_input)
                path = '/home/pi/Music/' + key_input
                for root, dirnames, files in os.walk(path):
                    for i in files:
                      Fullpath = join(root,i)
                      FileName = join(i)
                      if key_input in FileName:
                        if key_input.startswith(key_input):
                          #mp3file = join(key_input)
                          #f = os.path.join(root, key_input+'.mp3')
                          f = os.path.join(root, FileName)
                          print (f)
                player = subprocess.Popen(["omxplayer",f],stdin=subprocess.PIPE)
                fi = player.poll()
              elif key=='#':
                key_input = ''
              else:
                  key_input += key
                  #print (key)
                  #key_input.append(key)
                  print(key_input)
        if flag==1:
          key_input = ''
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
            #time.sleep(20)
            
            #break
            #player.stdin.write('q')      
            #st=1
        else:
          fi = player.poll()
          if (fi==0 and st==0):
            flag=1
            pt=pt+1
            if pt>h-1:
                pt=0
        sleep(0.1)
