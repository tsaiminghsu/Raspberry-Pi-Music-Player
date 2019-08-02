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
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Setup 74HC595 Shift Registor pins
DS   = 12     # Serial Data
SHCP = 21     # Clock
STCP = 20     # Latch
GPIO.setup(DS, GPIO.OUT)
GPIO.setup(SHCP, GPIO.OUT)
GPIO.setup(STCP, GPIO.OUT)
# Setup 7 segment display ,Q7 ~ Q1
seg = [[0,0,0,0,0,0,1],#0
       [1,0,0,1,1,1,1],#1
       [0,0,1,0,0,1,0],#2
       [0,0,0,0,1,1,0],#3
       [1,0,0,1,1,0,0],#4
       [0,1,0,0,1,0,0],#5
       [0,1,0,0,0,0,0],#6
       [0,0,0,1,1,1,1],#7
       [0,0,0,0,0,0,0],#8
       [0,0,0,0,1,0,0] #9
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
        digits = [[1,1,1,1,1,1,1], seg[unitDigit]]
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
try:
    for i in range(100):
        display(i,1)
        #print(str(display(i,1)))
        time.sleep(0.5)
    time.sleep(10)
finally:
    GPIO.cleanup()
