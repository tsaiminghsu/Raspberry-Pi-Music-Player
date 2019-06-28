import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD) 
rows= [24,25,26,20]
cols= [27,22,23]

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
    key = 0
    for col_num, col_pin in enumerate(cols):
        GPIO.output(col_pin, 1)
        for row_num, row_pin in enumerate(rows):
            if GPIO.input(row_pin):
               key = keys[row_num][col_num]
        GPIO.output(col_pin, 0)
    return key

while True:
    key = get_key()
    if key :
        print(key)
    time.sleep(0.2)
'''
def npscan(pin):
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(0.05)
    for inp in rows:
        if GPIO.input(inp):
            print keys[rows.index(inp)][cols.index(pin)],"key is pressed @",str(
inp),"/",str(pin)
            time.sleep(0.1)
    GPIO.output(pin, GPIO.LOW)
    time.sleep(0.05)
    return
 
try:
    GPIO.setmode(GPIO.BOARD)
    for pin in cols:
        GPIO.setup(pin, GPIO.OUT)
    for pin in rows:
        GPIO.setup(pin, GPIO.IN, GPIO.PUD_DOWN)
    while True:
        for pin in cols:
            npscan(pin)
except KeyboardInterrupt:
    GPIO.cleanup()
'''
