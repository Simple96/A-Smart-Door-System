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
import RPi.GPIO as GPIO
import subprocess
import sys
import pygame.mixer
import smtplib
from weather import Weather, Unit
from importlib import import_module
import os
from flask import Flask, render_template, Response, request
import io
import picamera
from base_camera import BaseCamera
import itchat

@itchat.msg_register(itchat.content.TEXT)
def get_msg(msg):
    global status_flag
    if msg.text == 'no':
        status_flag = 0
        itchat.logout()
    if msg.text == 'yes':
        status_flag = 3
        itchat.logout()
    print msg.text
    
class Camera(BaseCamera):
    global camera
    global camera_flag
    global x
    global y
    @staticmethod
    def frames():
        #with picamera.PiCamera() as camera:
            # let camera warm up
        
        while camera_flag:
            time.sleep(2)

            stream = io.BytesIO()
            for _ in camera.capture_continuous(stream, 'jpeg',
                                                 use_video_port=True):
                if camera_flag < 1:
                    break
                # return current frame
                stream.seek(0)
                yield stream.read()

                # reset stream for next frame
                stream.seek(0)
                stream.truncate()

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def index():
    global camera_flag
    global status_flag
    global start_web
    #if (time.time() - start_web) > 10:
    #    func = request.environ.get('werkzeug.server.shutdown')
    #    func()
        #shutdown_server()
    #    return
    
    """Video streaming home page."""
    print(request.method)
    if request.method == 'POST':
        if request.form.get('Open') == 'Open':
                # pass
            print("Open")
            #camera_flag = 0
            status_flag = 3
            #open_flag
            func = request.environ.get('werkzeug.server.shutdown')
            func()
            #shutdown_server()
            return render_template("success.html")
        elif  request.form.get('Reject') == 'Reject':
                # pass # do something else
            status_flag = 0
            print("Reject")
            func = request.environ.get('werkzeug.server.shutdown')
            func()
            return render_template("fail.html")
        else:
                # pass # unknown
            return render_template("index.html")
    elif request.method == 'GET':
            # return render_template("index.html")
            print("No Post Back Call")
    return render_template("index.html")


def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/contact',methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        if request.form['submit_button'] == 'Do Something':
            print("a")
            pass # do something
        elif request.form['submit_button'] == 'Do Something Else':
            print("b")
            pass # do something else
        else:
            pass # unknown
    elif request.method == 'GET':
        return render_template('contact.html', form=form)
##################################################################################################################
##########################################################
##################################################################################################################
def sendm():
    smtpUser = 'hs978xh344@gmail.com'
    smtpPass = 'ece5725!'

    toAdd='hs978@cornell.edu'#'xh344@cornell.edu'
    fromAdd = smtpUser

    subject = 'knock,knock http://172.20.10.4:5000/'#http://128.253.17.23:5000/'
    header = 'To: ' + toAdd + '\n' + 'From: ' + fromAdd + '\n' + 'Subject: ' + subject
    link='128,253,17,23:5000'
    body = 'check who is coming? '

    print header + '\n' + body

    s = smtplib.SMTP('smtp.gmail.com',587)
    s.ehlo()
    s.starttls()
    s.ehlo()

    s.login(smtpUser,smtpPass)
    s.sendmail(fromAdd, toAdd, header + '\n' + body)
    s.quit()
#white = 255,255,255
#black = 0,0,0




def register(name, str):
    file=open('/home/pi/final_project/password/'+name+'.txt',"w")
    file.write(str)




def changepw(str):
    file=open('/home/pi/final_project/password/hs.txt',"w")
    file.write(str)
    





def checkpw(id_, str):
    #str is the user input in GUI
    #if(id_==0):
        with open("/home/pi/final_project/password/hs.txt") as file:
            data1=file.read()
            
                #unlock the door call servo function
    
    #if(id_==1):
        with open("/home/pi/final_project/password/hxh.txt") as file:
            data2=file.read()
        
        return data1==str or data2==str
            
    #unlock the door call servo function





def train():
    recognizer = cv2.createLBPHFaceRecognizer()
    cascadePath= "/home/pi/final_project/opencv-master/data/haarcascades/haarcascade_frontalface_alt2.xml"
    face_cascade =cv2.CascadeClassifier(cascadePath)
# find the image directory
    BASE_DIR =os.path.dirname("/home/pi/final_project")
    image_dir =os.path.join(BASE_DIR, "final_project/images")
#print(image_dir)

#initialize the the trauning variable
    curr_id=0
    label_ids ={}
    y_labels=[]
    x_train=[]

    for root,dirs,files in os.walk(image_dir):
    
        for file in files :
      
           if file.endswith("jpg"):
                path = os.path.join(root,file)
                label =os.path.basename(root)
            #print(label)
            
                if not label in label_ids:
                    label_ids[label] = curr_id
                    curr_id=curr_id+1
                id_= label_ids[label]
            #print(label_ids)
                pil_image=Image.open(path).convert("L")# grayscale
                image_array = np.array(pil_image,"uint8")
            #print(image_array)
                faces=face_cascade.detectMultiScale(image_array, scaleFactor=1.5, minNeighbors=5,minSize=(5,5), flags= cv2.cv.CV_HAAR_SCALE_IMAGE)
            
                for(x,y,w,h) in faces:
                    roi= image_array[y:y+h,x:x+w]
                    x_train.append(roi)
                    y_labels.append(id_)

#print(x_train) just for check
    print(y_labels) 
# store the label
    with open("labels.pickle",'wb') as f:
        pickle.dump(label_ids,f)

#start to train
    recognizer.train(x_train,np.array(y_labels))
    recognizer.save("trainer.yml")







def gather_info():
    i=0
    im_num = 80
   
    rawCapture = PiRGBArray(camera,size=(480,320))
    face_cascade=cv2.CascadeClassifier('/home/pi/final_project/opencv-master/data/haarcascades/haarcascade_frontalface_alt2.xml')
    #time_start_l = time.time()
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port =True):
	#time_interval_l = time_now_l - time_start_l
	#if time_interval_l > 60:
        #    status_flag = 2

        #    return 0
	
	frame= frame.array
	gray =cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
	faces=face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5,minSize=(5,5), flags= cv2.cv.CV_HAAR_SCALE_IMAGE)
	for(x,y,w,h) in faces:
		print(x,y,w,h)
		rog= gray[y:y+h,x:x+w]# region of interets in gray scale
	    
	    # recognizer
                
		color1= (255,0,0)
		color2= (0,255,0)
		color3= (0,0,255)
		im=frame
		
		if(i<=im_num ):
                    cv2.imwrite('/home/pi/final_project/images/user2/'+str(i)+'.jpg', frame)#[y:y+h,x:x+h])
                    i=i+1
                else:
                    return 1
                cv2.rectangle(im,(x,y),(x+w,y+w),color1,2)
                    #cv2.imwrite('/home/pi/Desktop/test.jpg', frame[y:y+h,x:x+h])
                    #i = i+1
	#cv2.imshow('frame', frame)
        screen.fill(BLACK)################################
        sf=cv2.resize(frame,(280,240))
        sf= cv2.cvtColor(sf,cv2.COLOR_BGR2RGB)
        sf=np.rot90(sf)
        sf=pygame.surfarray.make_surface(sf)
        screen.blit(sf,(0,0))
        height = (240 * i) / im_num
        #print(height)
        pygame.draw.rect(screen,WHITE,[280,240 - height,40,height],0)
        pygame.display.flip()
	rawCapture.truncate(0)
    return 0
######################################################################
#   Function name: face_rec
#
#   Description: used for face detection in real time 
#                will break when a face is successfully detected
#
#   Made by: xh344
#
#   Date: 2018.11.27
######################################################################

def face_rec():
    # enable the picamera
    global status_flag
    global screen#################################
    global camera_flag
    global camera
    #if camera_flag == 0:

    rawCapture = PiRGBArray(camera,size=(480,320))
    
    record=0
    sum=0
    array=[]
    #input the face_cascade
    face_cascade=cv2.CascadeClassifier('/home/pi/final_project/opencv-master/data/haarcascades/haarcascade_frontalface_alt2.xml')
    #initialize the facerecognizer 
    recognizer = cv2.createLBPHFaceRecognizer()
    #load the traning data
    recognizer.load("trainer.yml")
    i = 0
    time_start_l = time.time()
    # capture frame by frame and detect and recognize the face frame by frame
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port =True):
        
        
	frame= frame.array
	gray =cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
	faces=face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5,minSize=(5,5), flags= cv2.cv.CV_HAAR_SCALE_IMAGE)
	time_now_l = time.time()
	time_interval_l = time_now_l - time_start_l
	if time_interval_l > 15:
            status_flag = 2
#            camera.close()
            return -1
	for(x,y,w,h) in faces:
		print(x,y,w,h)
	    # region of interets in gray scale
		rog= gray[y:y+h,x:x+w]
	    
	    # recognizer predict he id and the confidence number which associate with
                id_, conf = recognizer.predict(rog)    
            
            # after mutiple adjusting the confidence number, we use this region     
                if conf>= 35 and conf<=88:
                    print(id_)
                    array.append(id_)
                    if len(array)<=5:
                        sum=sum+id_
                    
                    else:
                        if sum>5:
                            status_flag = 3
                            #camera.close()
                            return 1
                        else:
                            status_flag = 3
                            #camera.close()
                            return 0
                        
                    #status_flag = 3 
                    #return -1
                    ###start to call checkpw function conbine with gui
	    # for different colors of retangular
		color1= (255,0,0)
		color2= (0,255,0)
		color3= (0,0,255)
		cv2.rectangle(frame,(x,y),(x+w,y+w),color1,2)
		#if(record == 0 ):
                    #cv2.imwrite('/home/pi/Desktop/datah/test'+str(i)+'.jpg', frame)#[y:y+h,x:x+h])
                    #cv2.imwrite('/home/pi/Desktop/test.jpg', frame[y:y+h,x:x+h])
                    #i = i+1
	#cv2.imshow('frame', frame)
		
	screen.fill(BLACK)################################
        sf=cv2.resize(frame,(320,240))
        sf= cv2.cvtColor(sf,cv2.COLOR_BGR2RGB)
        sf=np.rot90(sf)
        sf=pygame.surfarray.make_surface(sf)
        screen.blit(sf,(0,0))
        pygame.display.flip()
        
        
	rawCapture.truncate(0)
	
	# physical key for quiting
	if cv2.waitKey(20) & 0xFF ==ord('q'):
            break
    status_flag = 2
    #camera.close()
    return -1
######################################################################
#fun face_rec end here
######################################################################

def opend():
    global p_left
    global p_right
    
    vdd= 1.53
    dc = 100 * vdd / (vdd + 20)
    f = 1000 / (vdd + 20)

    vdd2= 1.47
    dc2 = 100 * vdd2 / (vdd2 + 20)
    f2 = 1000 / (vdd2 + 20)
    
    vdd3= 0
    dc3 = 100 * vdd3 / (vdd3 + 20)
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
        if time_interval > 1.2:
            break
        
    p_left.ChangeFrequency(f3)
    p_left.ChangeDutyCycle(dc3)
    
    p_right.ChangeFrequency(f3)
    p_right.ChangeDutyCycle(dc3)
    
def closed():
    global p_left
    global p_right
    
    vdd= 1.53
    dc = 100 * vdd / (vdd + 20)
    f = 1000 / (vdd + 20)

    vdd2= 1.47
    dc2 = 100 * vdd2 / (vdd2 + 20)
    f2 = 1000 / (vdd2 + 20)
    
    vdd3= 0
    dc3 = 100 * vdd3 / (vdd3 + 20)
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


os.putenv('SDL_VIDEODRIVER', 'fbcon') # Display on piTFT
os.putenv('SDL_FBDEV', '/dev/fb1')
os.putenv('SDL_MOUSEDRV', 'TSLIB') # Track mouse clicks on piTFT
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')
GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.IN)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
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
    

camera= PiCamera()
#camera = pygame.camera.Camera()
camera.resolution=(480,320)
camera.framerate=64
#camera_flag = 1
#register("hxh",str(1111))
#register("hs",str(1111))
s1 = "espeak '"
s = "hello"
s3 = "' --stdout | aplay -D plughw:1,0"
str_out = s1 + s + s3
os.system("espeak 'system starts' --stdout | aplay -D plughw:1,0")
pygame.init()
#pygame.camera.init()
pygame.mouse.set_visible(False)
WHITE = 255, 255, 255
BLACK = 0,0,0
size = width, height =320,240
screen = pygame.display.set_mode(size)
sleep_time=0.003

my_font_big = pygame.font.Font(None, 30)
my_font_key = pygame.font.Font(None, 20)
my_font_info = pygame.font.Font(None, 14)
my_font_num = pygame.font.Font(None, 60)

my_button_s1 = {(240,60):'Enter',(240,180):'Register',(60,180):'Quit',(150,180):'Voice',(240,120):'SetPW',(60,120):'Wechat',(150,120):'Knock'}
my_inform = {(80,180):'Press Button to enter'}
my_warning = {(160,120):'Facial Rec...'}
my_warning1 = {(160,120):'Processing...'}
my_warning2 = {(160,120):'^_^ Welcome ^_^'}
my_warning3 = {(160,120):'Waiting for web control'}
my_warning4 = {(160,100):'E-mail has been sent',(160,140):'Waiting for response throught port 5000'}
my_warning5 = {(160,120):'Please speak'}

my_number = {(30,90):'7',(30,150):'4',(30,210):'1',(90,90):'8',(90,150):'5',(90,210):'2',(150,90):'9',(150,150):'6',(150,210):'3',(210,150):'0'}
my_main_button = {(280,30):'M',(280,90):'A',(280,150):'I',(280,210):'N'}
my_code = {(30,30):'',(90,30):'',(150,30):'',(210,30):''}

my_message1 = {(160,7):'logining in to Wechat...'}
my_message2 = {(160,7):'logining in to Wechat...',(160,21):'login succeed',(160,35):'Sending message...'}
my_message3 = {(160,7):'logining in to Wechat...',(160,21):'login succeed',(160,35):'Sending message...',(160,49):'Message sent, waiting for response'}

x = 0
y = 0
flag_sys = 1
time_start=time.time()

mic = pygame.image.load("mic.png")
mic_rect = mic.get_rect()
mic_rect.center = [160,120]

snow = pygame.image.load("snow.png")
snow_rect = snow.get_rect()
snow_rect.center = [150,60]

thunder = pygame.image.load("thunder.png")
thunder_rect = thunder.get_rect()
thunder_rect.center = [150,60]

fog = pygame.image.load("fog.png")
fog_rect = fog.get_rect()
fog_rect.center = [150,60]

cloud = pygame.image.load("cloudy.png")
cloud_rect = cloud.get_rect()
cloud_rect.center = [150,60]

sun = pygame.image.load("sun.png")
sun_rect = sun.get_rect()
sun_rect.center = [150,60]

arrow = pygame.image.load("arrow.png")
arrow_rect = arrow.get_rect()
arrow_rect.center = [210,210]

deletea = pygame.image.load("delete.png")
deletea_rect = arrow.get_rect()
deletea_rect.center = [210,90]

#Degree = {(40,60):'2 CEL'}

weather_flag = 1
status_flag = 0
ID = 1
camera_flag = 0
speak_flag = 0
open_flag = 0

enter_num = 0

weather = Weather(unit = Unit.CELSIUS)
location = weather.lookup_by_location('Ithaca')
code = location.condition.code
if code < 5:#thunder
    weather_flag = 0
if code > 4 and code < 13:#snow
    weather_flag = 1
if code > 12 and code < 19:#rain
    weather_flag = 2
if code > 18 and code < 23:#foggy
    weather_flag = 3
if code > 22 and code < 31:#cloudy
    weather_flag = 4
if code > 30 and code < 37:#sunny
    weather_flag = 5
if code > 36:#thunder
    weather_flag = 0
#weather_flag = 5
temp = str(location.condition.temp) + ' CEL'
Degree = {(60,50):temp}
my_loc = {(60,70):'Ithaca, NY'}

try:
    while flag_sys:
        while status_flag == 0:
            screen.fill(BLACK)
            time_now = time.time()
            pygame.draw.rect(screen,WHITE,[210,40,60,40],0)
            pygame.draw.rect(screen,WHITE,[210,160,60,40],0)
            pygame.draw.rect(screen,WHITE,[210,100,60,40],0)
            pygame.draw.rect(screen,WHITE,[30,100,60,40],0)
            pygame.draw.rect(screen,WHITE,[120,100,60,40],0)
            pygame.draw.rect(screen,WHITE,[30,160,60,40],0)
            pygame.draw.rect(screen,WHITE,[120,160,60,40],0)
            
            localtime = time.asctime(time.localtime(time.time()))
            #time display
            text_surface = my_font_key.render(localtime, True, WHITE)
            rect = text_surface.get_rect(center=(50,10))
            screen.blit(text_surface, rect)
            #print(type(localtime))
            for text_pos, my_text in Degree.items():
                text_surface = my_font_big.render(my_text, True, WHITE)
                rect = text_surface.get_rect(center=text_pos)
                screen.blit(text_surface, rect)
        
        
            for text_pos, my_text in my_button_s1.items():
                text_surface = my_font_key.render(my_text, True, BLACK)
                rect = text_surface.get_rect(center=text_pos)
                screen.blit(text_surface, rect)
            
            for text_pos, my_text in my_loc.items():
                text_surface = my_font_key.render(my_text, True, WHITE)
                rect = text_surface.get_rect(center=text_pos)
                screen.blit(text_surface, rect)
            #for text_pos, my_text in my_inform.items():
            #    text_surface = my_font_key.render(my_text, True, WHITE)
            #    rect = text_surface.get_rect(center=text_pos)
            #    screen.blit(text_surface, rect)
            
            if(weather_flag == 0):
                #screen.fill(BLACK)
                screen.blit(thunder, thunder_rect)
            if(weather_flag == 1):
                #screen.fill(BLACK)
                screen.blit(rain, rain_rect)            
            if(weather_flag == 2):
                #screen.fill(BLACK)
                screen.blit(snow, snow_rect)
            if(weather_flag == 3):
                #screen.fill(BLACK)
                screen.blit(fog, fog_rect)
            if(weather_flag == 4):
                #screen.fill(BLACK)
                screen.blit(cloudy, cloudy_rect)
            if(weather_flag == 5):
                #screen.fill(BLACK)
                screen.blit(sun, sun_rect)
                
            pygame.display.flip()
            
            for event in pygame.event.get():
                if(event.type is MOUSEBUTTONDOWN):
                    pos = pygame.mouse.get_pos()
                elif(event.type is MOUSEBUTTONUP):
                    pos = pygame.mouse.get_pos()
                    x,y = pos
                    
            if x > 210 and x < 270 and y > 40 and y < 80:
                status_flag = 1
                x = 0
                y = 0
                
            if x > 210 and x < 270 and y > 160 and y < 200:
                status_flag = 4
                x = 0
                y = 0
                
            if x > 210 and x < 270 and y > 100 and y < 140:
                status_flag = 6
                x = 0
                y = 0
            
            if x > 120 and x < 180 and y > 100 and y < 140:
                status_flag = 8
                x = 0
                y = 0
                
            if x > 210 and x < 270 and y > 100 and y < 140:
                status_flag = 9
                x = 0
                y = 0
            
            if x > 30 and x < 90 and y > 100 and y < 140:
                status_flag = 10
                x = 0
                y = 0
                
            if x > 120 and x < 180 and y > 160 and y < 200:
                status_flag = 11
                x = 0
                y = 0
            
            if x > 30 and x < 90 and y > 160 and y < 200:
                status_flag = 12
                flag_sys = 0
                x = 0
                y = 0
                
        while status_flag == 1:
            s = "Hi, please look at the camera!"
            str_out = s1 + s + s3
            os.system(str_out)
            screen.fill(BLACK)
            for text_pos, my_text in my_warning.items():
                text_surface = my_font_big.render(my_text, True, WHITE)
                rect = text_surface.get_rect(center=text_pos)
                screen.blit(text_surface, rect)
            pygame.display.flip()
            ID = face_rec()
            print("out")
            
        speak_flag == 0
        while status_flag == 2:
            if speak_flag == 0:
                s = "Sorry, can't recognize your face, please enter password to get in"
                speak_flag = 1
                str_out = s1 + s + s3
                os.system(str_out)
            
            screen.fill(BLACK)
            pygame.draw.rect(screen,WHITE,[240,0,80,240],0)
            for text_pos, my_text in my_number.items():
                text_surface = my_font_num.render(my_text, True, WHITE)
                rect = text_surface.get_rect(center=text_pos)
                screen.blit(text_surface, rect)
            for text_pos, my_text in my_main_button.items():
                text_surface = my_font_num.render(my_text, True, BLACK)
                rect = text_surface.get_rect(center=text_pos)
                screen.blit(text_surface, rect)
            for text_pos, my_text in my_code.items():
                text_surface = my_font_num.render(my_text, True, WHITE)
                rect = text_surface.get_rect(center=text_pos)
                screen.blit(text_surface, rect)
            
            screen.blit(arrow, arrow_rect)
            screen.blit(deletea, deletea_rect)
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if(event.type is MOUSEBUTTONDOWN):
                    pos = pygame.mouse.get_pos()
                elif(event.type is MOUSEBUTTONUP):
                    pos = pygame.mouse.get_pos()
                    x,y = pos
                
            if x < 180 and y > 60 and enter_num < 4:
                if y > 180:
                    if x < 60:
                        my_code[(30 + enter_num * 60,30)] = "1"
                    if x > 60 and x < 120:
                        my_code[(30 + enter_num * 60,30)] = "2"
                    if x > 120:
                        my_code[(30 + enter_num * 60,30)] = "3"
                        
                if y > 120 and y < 180:
                    if x < 60:
                        my_code[(30 + enter_num * 60,30)] = "4"
                    if x > 60 and x < 120:
                        my_code[(30 + enter_num * 60,30)] = "5"
                    if x > 120:
                        my_code[(30 + enter_num * 60,30)] = "6"
                        
                if y > 60 and y < 120:
                    if x < 60:
                        my_code[(30 + enter_num * 60,30)] = "7"
                    if x > 60 and x < 120:
                        my_code[(30 + enter_num * 60,30)] = "8"
                    if x > 120:
                        my_code[(30 + enter_num * 60,30)] = "9"
                        
                enter_num = enter_num + 1
                x = 0
                y = 0
             
             
             
             
            if x > 180 and x < 240 and y > 120 and y < 180 and enter_num < 4:
                my_code[(30 + enter_num * 60,30)] = "0"
                enter_num = enter_num + 1
                x = 0
                y = 0
                
            if x > 180 and x < 240 and y > 60 and y < 120 and enter_num > 0:
                enter_num = enter_num - 1
                my_code[(30 + enter_num * 60,30)] = ""
                x = 0
                y = 0
                
            if x > 180 and x < 240 and y > 180:
                str_code = my_code[(30,30)] + my_code[(90,30)] + my_code[(150,30)] + my_code[(210,30)]
                print(ID)
                check_result = checkpw(ID, str_code)
                print(check_result)
                if check_result == 1:
                    my_code[(30,30)] = ''
                    my_code[(90,30)] = ''
                    my_code[(150,30)] = ''
                    my_code[(210,30)] = ''
                    enter_num = 0
                    status_flag = 3
                x = 0
                y = 0
            if x > 240:
                my_code[(30,30)] = ''
                my_code[(90,30)] = ''
                my_code[(150,30)] = ''
                my_code[(210,30)] = ''
                enter_num = 0
                status_flag = 0
                x = 0
                y = 0
        
        
        time_start=time.time()
        while status_flag == 3:
            s = "Welcome"
            str_out = s1 + s + s3
            os.system(str_out)
            #sendm()
            screen.fill(BLACK)
            for text_pos, my_text in my_warning2.items():
                text_surface = my_font_big.render(my_text, True, WHITE)
                rect = text_surface.get_rect(center=text_pos)
                screen.blit(text_surface, rect)
            pygame.display.flip()
            opend()
            time.sleep(3)
            iii = 0
            while GPIO.input(26):
                iii = iii + 1
                print(iii)
            closed()
            status_flag = 0
            #time_now = time.time()
            #time_interval = time_now - time_start
            #if time_interval > 10:
            #    status_flag = 0
        
        speak_flag = 0
        while status_flag == 4:
            if speak_flag == 0:
                s = "Hello, please enter password to register"
                speak_flag = 1
                str_out = s1 + s + s3
                os.system(str_out)
            screen.fill(BLACK)
            pygame.draw.rect(screen,WHITE,[240,0,80,240],0)
            for text_pos, my_text in my_number.items():
                text_surface = my_font_num.render(my_text, True, WHITE)
                rect = text_surface.get_rect(center=text_pos)
                screen.blit(text_surface, rect)
            for text_pos, my_text in my_main_button.items():
                text_surface = my_font_num.render(my_text, True, BLACK)
                rect = text_surface.get_rect(center=text_pos)
                screen.blit(text_surface, rect)
            for text_pos, my_text in my_code.items():
                text_surface = my_font_num.render(my_text, True, WHITE)
                rect = text_surface.get_rect(center=text_pos)
                screen.blit(text_surface, rect)
            
            screen.blit(arrow, arrow_rect)
            screen.blit(deletea, deletea_rect)
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if(event.type is MOUSEBUTTONDOWN):
                    pos = pygame.mouse.get_pos()
                elif(event.type is MOUSEBUTTONUP):
                    pos = pygame.mouse.get_pos()
                    x,y = pos
                    
            if x < 180 and y > 60 and enter_num < 4:
                if y > 180:
                    if x < 60:
                        my_code[(30 + enter_num * 60,30)] = "1"
                    if x > 60 and x < 120:
                        my_code[(30 + enter_num * 60,30)] = "2"
                    if x > 120:
                        my_code[(30 + enter_num * 60,30)] = "3"
                        
                if y > 120 and y < 180:
                    if x < 60:
                        my_code[(30 + enter_num * 60,30)] = "4"
                    if x > 60 and x < 120:
                        my_code[(30 + enter_num * 60,30)] = "5"
                    if x > 120:
                        my_code[(30 + enter_num * 60,30)] = "6"
                        
                if y > 60 and y < 120:
                    if x < 60:
                        my_code[(30 + enter_num * 60,30)] = "7"
                    if x > 60 and x < 120:
                        my_code[(30 + enter_num * 60,30)] = "8"
                    if x > 120:
                        my_code[(30 + enter_num * 60,30)] = "9"
                        
                enter_num = enter_num + 1
                x = 0
                y = 0
            if x > 180 and x < 240 and y > 120 and y < 180 and enter_num < 4:
                my_code[(30 + enter_num * 60,30)] = "0"
                enter_num = enter_num + 1
                x = 0
                y = 0
                
            if x > 180 and x < 240 and y > 60 and y < 120 and enter_num > 0:
                enter_num = enter_num - 1
                my_code[(30 + enter_num * 60,30)] = ""
                x = 0
                y = 0
                
            if x > 180 and x < 240 and y > 180:
                str_code = my_code[(30,30)] + my_code[(90,30)] + my_code[(150,30)] + my_code[(210,30)]
                print(ID)
                check_result = checkpw(ID, str_code)
                print(check_result)
                if check_result == 1:
                    my_code[(30,30)] = ''
                    my_code[(90,30)] = ''
                    my_code[(150,30)] = ''
                    my_code[(210,30)] = ''
                    enter_num = 0
                    status_flag = 5
                x = 0
                y = 0
            if x > 240:
                my_code[(30,30)] = ''
                my_code[(90,30)] = ''
                my_code[(150,30)] = ''
                my_code[(210,30)] = ''
                enter_num = 0
                status_flag = 0
                x = 0
                y = 0
                
        speak_flag = 0        
        while status_flag == 5:
            if speak_flag == 0:
                s = "please look at the camera to help me gather information about you"
                speak_flag = 1
                str_out = s1 + s + s3
                os.system(str_out)
            screen.fill(BLACK)
            #showing :  strating collecting info here
            pygame.display.flip()
            gather_info_success_flag = 0
            gather_info_success_flag = gather_info()
            if gather_info_success_flag:
                s = "information gathered successfully, please wait"
                str_out = s1 + s + s3
                os.system(str_out)
                screen.fill(BLACK)
                #showing :  training now, please wait
                for text_pos, my_text in my_warning1.items():
                    text_surface = my_font_num.render(my_text, True, WHITE)
                    rect = text_surface.get_rect(center=text_pos)
                    screen.blit(text_surface, rect)
                
                pygame.display.flip()
                train()
                print("train out")
                gather_info_success_flag = 0
                status_flag = 0
        
        speak_flag = 0 
        while status_flag == 6:
            if speak_flag == 0:
                s = "please enter your old password"
                speak_flag = 1
                str_out = s1 + s + s3
                os.system(str_out)
            screen.fill(WHITE)
            pygame.draw.rect(screen,BLACK,[240,0,80,240],0)
            for text_pos, my_text in my_number.items():
                text_surface = my_font_num.render(my_text, True, BLACK)
                rect = text_surface.get_rect(center=text_pos)
                screen.blit(text_surface, rect)
            for text_pos, my_text in my_main_button.items():
                text_surface = my_font_num.render(my_text, True, WHITE)
                rect = text_surface.get_rect(center=text_pos)
                screen.blit(text_surface, rect)
            for text_pos, my_text in my_code.items():
                text_surface = my_font_num.render(my_text, True, BLACK)
                rect = text_surface.get_rect(center=text_pos)
                screen.blit(text_surface, rect)
            
            screen.blit(arrow, arrow_rect)
            screen.blit(deletea, deletea_rect)
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if(event.type is MOUSEBUTTONDOWN):
                    pos = pygame.mouse.get_pos()
                elif(event.type is MOUSEBUTTONUP):
                    pos = pygame.mouse.get_pos()
                    x,y = pos
                
            if x < 180 and y > 60 and enter_num < 4:
                if y > 180:
                    if x < 60:
                        my_code[(30 + enter_num * 60,30)] = "1"
                    if x > 60 and x < 120:
                        my_code[(30 + enter_num * 60,30)] = "2"
                    if x > 120:
                        my_code[(30 + enter_num * 60,30)] = "3"
                        
                if y > 120 and y < 180:
                    if x < 60:
                        my_code[(30 + enter_num * 60,30)] = "4"
                    if x > 60 and x < 120:
                        my_code[(30 + enter_num * 60,30)] = "5"
                    if x > 120:
                        my_code[(30 + enter_num * 60,30)] = "6"
                        
                if y > 60 and y < 120:
                    if x < 60:
                        my_code[(30 + enter_num * 60,30)] = "7"
                    if x > 60 and x < 120:
                        my_code[(30 + enter_num * 60,30)] = "8"
                    if x > 120:
                        my_code[(30 + enter_num * 60,30)] = "9"
                        
                enter_num = enter_num + 1
                x = 0
                y = 0
            if x > 180 and x < 240 and y > 120 and y < 180 and enter_num < 4:
                my_code[(30 + enter_num * 60,30)] = "0"
                enter_num = enter_num + 1
                x = 0
                y = 0
                
            if x > 180 and x < 240 and y > 60 and y < 120 and enter_num > 0:
                enter_num = enter_num - 1
                my_code[(30 + enter_num * 60,30)] = ""
                x = 0
                y = 0
            if x > 180 and x < 240 and y > 180:
                str_code = my_code[(30,30)] + my_code[(90,30)] + my_code[(150,30)] + my_code[(210,30)]
                print(ID)
                check_result = checkpw(ID, str_code)
                print(check_result)
                if check_result == 1:
                    s = "correct password"                  
                    str_out = s1 + s + s3
                    os.system(str_out)
                    my_code[(30,30)] = ''
                    my_code[(90,30)] = ''
                    my_code[(150,30)] = ''
                    my_code[(210,30)] = ''
                    enter_num = 0
                    status_flag = 7
                x = 0
                y = 0
            if x > 240:
                my_code[(30,30)] = ''
                my_code[(90,30)] = ''
                my_code[(150,30)] = ''
                my_code[(210,30)] = ''
                enter_num = 0
                status_flag = 0
                x = 0
                y = 0
                
        speak_flag = 0        
        while status_flag == 7:
            if speak_flag == 0:
                s = "please enter your new password"
                speak_flag = 1
                str_out = s1 + s + s3
                os.system(str_out)
            screen.fill(WHITE)
            pygame.draw.rect(screen,BLACK,[240,0,80,240],0)
            for text_pos, my_text in my_number.items():
                text_surface = my_font_num.render(my_text, True, BLACK)
                rect = text_surface.get_rect(center=text_pos)
                screen.blit(text_surface, rect)
            for text_pos, my_text in my_main_button.items():
                text_surface = my_font_num.render(my_text, True, WHITE)
                rect = text_surface.get_rect(center=text_pos)
                screen.blit(text_surface, rect)
            for text_pos, my_text in my_code.items():
                text_surface = my_font_num.render(my_text, True, BLACK)
                rect = text_surface.get_rect(center=text_pos)
                screen.blit(text_surface, rect)
            
            screen.blit(arrow, arrow_rect)
            screen.blit(deletea, deletea_rect)
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if(event.type is MOUSEBUTTONDOWN):
                    pos = pygame.mouse.get_pos()
                elif(event.type is MOUSEBUTTONUP):
                    pos = pygame.mouse.get_pos()
                    x,y = pos
                    
            if x < 180 and y > 60 and enter_num < 4:
                if y > 180:
                    if x < 60:
                        my_code[(30 + enter_num * 60,30)] = "1"
                    if x > 60 and x < 120:
                        my_code[(30 + enter_num * 60,30)] = "2"
                    if x > 120:
                        my_code[(30 + enter_num * 60,30)] = "3"
                        
                if y > 120 and y < 180:
                    if x < 60:
                        my_code[(30 + enter_num * 60,30)] = "4"
                    if x > 60 and x < 120:
                        my_code[(30 + enter_num * 60,30)] = "5"
                    if x > 120:
                        my_code[(30 + enter_num * 60,30)] = "6"
                        
                if y > 60 and y < 120:
                    if x < 60:
                        my_code[(30 + enter_num * 60,30)] = "7"
                    if x > 60 and x < 120:
                        my_code[(30 + enter_num * 60,30)] = "8"
                    if x > 120:
                        my_code[(30 + enter_num * 60,30)] = "9"
                        
                enter_num = enter_num + 1
                x = 0
                y = 0
            if x > 180 and x < 240 and y > 120 and y < 180 and enter_num < 4:
                my_code[(30 + enter_num * 60,30)] = "0"
                enter_num = enter_num + 1
                x = 0
                y = 0
                
            if x > 180 and x < 240 and y > 60 and y < 120 and enter_num > 0:
                enter_num = enter_num - 1
                my_code[(30 + enter_num * 60,30)] = ""
                x = 0
                y = 0
            if x > 180 and x < 240 and y > 180:
                str_code = my_code[(30,30)] + my_code[(90,30)] + my_code[(150,30)] + my_code[(210,30)]
                if my_code[(30,30)] != "" and my_code[(90,30)] != "" and my_code[(150,30)] != "" and my_code[(210,30)] != "":
                #print(ID)
                #check_result = checkpw(ID, str_code)
                #print(check_result)
                #if check_result == 1:
                    my_code[(30,30)] = ''
                    my_code[(90,30)] = ''
                    my_code[(150,30)] = ''
                    my_code[(210,30)] = ''
                    changepw(str_code)
                    s = "password reset succeed"
                    str_out = s1 + s + s3
                    os.system(str_out)
                    enter_num = 0
                    status_flag = 0
                    
                x = 0
                y = 0
            if x > 240:
                my_code[(30,30)] = ''
                my_code[(90,30)] = ''
                my_code[(150,30)] = ''
                my_code[(210,30)] = ''
                enter_num = 0
                status_flag = 0
                x = 0
                y = 0
        
        speak_flag == 0
        while status_flag == 8:
            if speak_flag == 0:
                s = "E-mail has been sent to the owner, waiting for response now"
                speak_flag = 1
                str_out = s1 + s + s3
                os.system(str_out)
            screen.fill(BLACK)
            for text_pos, my_text in my_warning4.items():
                text_surface = my_font_info.render(my_text, True, WHITE)
                rect = text_surface.get_rect(center=text_pos)
                screen.blit(text_surface, rect)
            pygame.display.flip()
            #$start_web = time.time()
            sendm()
            camera_flag = 3
            app.run(host="0.0.0.0", threaded=True)
        
        while status_flag == 9:
            sub_flag = 1
            while sub_flag:
                screen.fill(BLACK)
                for text_pos, my_text in my_warning4.items():
                    text_surface = my_font_info.render(my_text, True, WHITE)
                    rect = text_surface.get_rect(center=text_pos)
                    screen.blit(text_surface, rect)
                pygame.display.flip()
        
        speak_flag == 0
        while status_flag == 10:
            if speak_flag == 0:
                s = "Use wechat to login"
                speak_flag = 1
                str_out = s1 + s + s3
                os.system(str_out)
                
            screen.fill(WHITE)
            ii = 0
            for text_pos, my_text in my_message1.items():
                text_surface = my_font_info.render(my_text, True, BLACK)
                rect = text_surface.get_rect(center=text_pos)
                screen.blit(text_surface, rect)
                
            pygame.display.flip()
            #itchat.get_QR(picDir='./qr.png')
            itchat.login(screen = screen, picDir = './qr.png')
            #qr = pygame.image.load('./qr.png')
            #qr = pygame.transform.scale(qr,(200,200))
            #screen.blit(qr,(120,40))
            #itchat.login(picDir = './qr.png')
            
           
            for text_pos, my_text in my_message2.items():
                text_surface = my_font_info.render(my_text, True, BLACK)
                rect = text_surface.get_rect(center=text_pos)
                screen.blit(text_surface, rect)
                
            pygame.display.flip()
            camera.capture('./realtime.jpg')
            itchat.send('Let that guy get in? [yes/no]', toUserName = 'filehelper')
            itchat.send_image('./realtime.jpg',toUserName = 'filehelper')
            
        
            for text_pos, my_text in my_message3.items():
                text_surface = my_font_info.render(my_text, True, BLACK)
                rect = text_surface.get_rect(center=text_pos)
                screen.blit(text_surface, rect)
                #ii = ii + 1
               
            pygame.display.flip()
            itchat.start_receiving()
            itchat.run()
        
        speak_flag = 0
        if status_flag == 11:
            timea = time.time()
        while status_flag == 11:
            if speak_flag == 0:
                s = "Voice recognition part porbiddened due to sound card conflict, sorry"
                speak_flag = 1
                str_out = s1 + s + s3
                os.system(str_out)
            screen.fill(WHITE)
            screen.blit(mic, mic_rect)
            pygame.display.flip()
            with open("/home/pi/final_project/voiceorder.txt") as file:
                data1=file.read()
                file.close()
                ti = time.time()-timea
                if ti >10:
                    status_flag = 0
                    break
                #print (data1)
                if data1 == 'open':
                    print('^_^')
                    status_flag = 3
                    break
            #i=i+1
            
except KeyboardInterrupt:
    pass        

p_left.stop()
p_right.stop()
GPIO.cleanup()













