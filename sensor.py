import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.IN)

try:
    i = 1
    time.sleep(1)
    while True:
        if GPIO.input(26):
            print(i)
            i = i + 1
            time.sleep(0.1)
        time.sleep(0.1)
        
except:
    pass

GPIO.cleanup()