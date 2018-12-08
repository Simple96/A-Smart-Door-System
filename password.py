import os
i=0
flag = 1
while flag:
    with open("/home/pi/final_project/voiceorder.txt") as file:
            data1=file.read()
            file.close()
            #print (data1)
            if data1 == 'open':
                print('^_^')
                flag = 0
                break
            i=i+1