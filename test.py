from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import os
import numpy as np
from  PIL import Image
import pickle
import pygame
from pygame.locals import *
camera= PiCamera()
camera.resolution=(480,320)
camera.framerate=64
rawCapture = PiRGBArray(camera,size=(480,320))
face_cascade=cv2.CascadeClassifier('/home/pi/final_project/opencv-master/data/haarcascades/haarcascade_frontalface_alt2.xml')
i=0
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port =True):
   
	
    frame= frame.array
    gray =cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces=face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5,minSize=(5,5), flags= cv2.cv.CV_HAAR_SCALE_IMAGE)
    for(x,y,w,h) in faces:
	    print(x,y,w,h)
	    rog= gray[y:y+h,x:x+w]# region of interets in gray scale
	    
	    # recognizer
            #id_, conf = recognizer.predict(rog)    
            #if conf>= 45 and conf<=88:
            #   print(id_)
	    color1= (255,0,0)
	    color2= (0,255,0)
	    color3= (0,0,255)
	    cv2.rectangle(frame,(x,y),(x+w,y+w),color1,2)
	    if(i<=80 ):
                cv2.imwrite('/home/pi/final_project/images/user2/'+str(i)+'.jpg', frame)#[y:y+h,x:x+h])
                i=i+1
                    #cv2.imwrite('/home/pi/Desktop/test.jpg', frame[y:y+h,x:x+h])
                    #i = i+1
    cv2.imshow('frame', frame)
    rawCapture.truncate(0)
    if cv2.waitKey(20) & 0xFF ==ord('q'):
            break