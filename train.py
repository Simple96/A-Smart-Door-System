import cv2
import os
import numpy as np
from  PIL import Image
import pickle
#use LBPH FACE REcogizer providedby opencv
recognizer = cv2.createLBPHFaceRecognizer()
cascadePath= "/home/pi/final_project/opencv-master/data/haarcascades/haarcascade_frontalface_alt2.xml"
face_cascade =cv2.CascadeClassifier(cascadePath)

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
#print(y_labels) just for check
# store the label
with open("labels.pickle",'wb') as f:
    pickle.dump(label_ids,f)

#start to train
recognizer.train(x_train,np.array(y_labels))
recognizer.save("trainer.yml")

