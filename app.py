#!/usr/bin/env python
from importlib import import_module
import os
from flask import Flask, render_template, Response, request
import io
import time
import picamera
from base_camera import BaseCamera
from picamera.array import PiRGBArray
from picamera import PiCamera
import pygame

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


# import camera driver
#if os.environ.get('CAMERA'):
#    Camera = import_module('camera_' + os.environ['CAMERA']).Camera
#else:
#    from camera import Camera

# Raspberry Pi camera module (requires picamera package)
#from camera_pi import Camera
#from picamera.array import PiRGBArray
#from picamera import PiCamera

app = Flask(__name__)


#@app.route('/')
#def index():
#    """Video streaming home page."""
#    return render_template('index.html')

@app.route("/", methods=['GET', 'POST'])
def index():
    global camera_flag
    """Video streaming home page."""
    print(request.method)
    if request.method == 'POST':
        if request.form.get('Encrypt') == 'Encrypt':
                # pass
            print("Encrypted")
            camera_flag = 0
            func = request.environ.get('werkzeug.server.shutdown')
            func()
            #shutdown_server()
            return
        elif  request.form.get('Decrypt') == 'Decrypt':
                # pass # do something else
            print("Decrypted")
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

if __name__ == '__main__':
    camera= PiCamera()
    #camera = pygame.camera.Camera()
    camera.resolution=(480,320)
    camera.framerate=64
    camera_flag = 1
    app.run(host="0.0.0.0", threaded=True)
    
    
    while True:
        BLACK = 0,0,0
        x = 0
        y = 0
        screen = pygame.display.set_mode((320,240))
        screen.fill(BLACK)
        pygame.display.flip()
    
    
    WHITE = 0,0,0
    x = 0
    y = 0
    screen = pygame.display.set_mode((320,240))
    screen.fill(WHITE)
    pygame.display.flip()
