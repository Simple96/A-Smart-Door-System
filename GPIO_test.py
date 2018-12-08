import pygame
import RPi.GPIO as GPIO
import time
import subprocess


def open():
    global p_left
    global p_right
    
    vdd= 1.53
    dc = 100 * vdd / (vdd + 20)
    f = 1000 / (vdd + 20)

    vdd2= 1.47
    dc2 = 100 * vdd2 / (vdd2 + 20)
    f2 = 1000 / (vdd2 + 20)
    
    vdd3= 0
    dc3 = 100 * vdd2 / (vdd3 + 20)
    f3 = 1000 / (vdd3 + 20)

    p_left.ChangeFrequency(f)
    p_left.ChangeDutyCycle(dc)
    
    p_right.ChangeFrequency(f2)
    p_right.ChangeDutyCycle(dc2)
    
    #p_left.start(dc)
    #p_right.start(dc2)
    time_start=time.time()
    
    while 1:
        time_now=time.time()
        time_interval=time_now-time_start
        if time_interval > 0.9:
            break
        
    p_left.ChangeFrequency(f3)
    p_left.ChangeDutyCycle(dc3)
    
    p_right.ChangeFrequency(f3)
    p_right.ChangeDutyCycle(dc3)
    
def close():
    global p_left
    global p_right
    
    vdd= 1.53
    dc = 100 * vdd / (vdd + 20)
    f = 1000 / (vdd + 20)

    vdd2= 1.47
    dc2 = 100 * vdd2 / (vdd2 + 20)
    f2 = 1000 / (vdd2 + 20)
    
    vdd3= 0
    dc3 = 100 * vdd2 / (vdd3 + 20)
    f3 = 1000 / (vdd3 + 20)

    p_left.ChangeFrequency(f2)
    p_left.ChangeDutyCycle(dc2)
    
    p_right.ChangeFrequency(f)
    p_right.ChangeDutyCycle(dc)
    
    #p_left.start(dc2) 
    #p_right.start(dc)
    time_start=time.time()
    
    while 1:
        time_now=time.time()
        time_interval=time_now-time_start
        if time_interval > 1:
            break
        
    #p_left.stop()
    #p_right.stop()
    p_left.ChangeFrequency(f3)
    p_left.ChangeDutyCycle(dc3)
    
    p_right.ChangeFrequency(f3)
    p_right.ChangeDutyCycle(dc3)



my_flag = 1
GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(26, GPIO.IN)

try:
    #time_start=time.time()
    #while my_flag:
    #    i = 1
    #    time_now=time.time()
    #    time_interval=time_now-time_start
    #    if time_interval > 0.8:
    #        breakvdd= 1.53
    
    vdd= 0
    dc = 100 * vdd / (vdd + 20)
    f = 1000 / (vdd + 20)

    vdd2= 0
    dc2 = 100 * vdd2 / (vdd2 + 20)
    f2 = 1000 / (vdd2 + 20)
    
    #vdd3 = 0
    #dc3 = 100 * vdd3 / (vdd3 + 20)
    #f3 = 1000 / (vdd3 + 20)
    
    p_left = GPIO.PWM(5,f)
    p_left.start(dc2)
    p_right = GPIO.PWM(13,f2)
    p_right.start(dc2)
    
    open()
    time.sleep(1)
    i = 1
    while GPIO.input(26):
        i = i + 1
        print(i)
    close()
    
    while True:
        i = 1
        
except KeyboardInterrupt:
    pass

p_left.stop()
p_right.stop()
GPIO.cleanup()