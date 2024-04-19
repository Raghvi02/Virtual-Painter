import numpy as np
import cv2
import time
import os
import mod as htm
folderPath="images"
myList=os.listdir(folderPath)

overlayList=[]
for imPath in myList:
    image= cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)
header= overlayList[0]

cap= cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)
detector= htm.Detector()
xp=0
yp=0   
imgCanvas= np.zeros((720,1280,3),np.uint8)
drawColor=(255,255,255)
lmlist=[]
while True:
    #1 import image
    success,img= cap.read()
    img = cv2.flip(img,1)
    #2 find hand landmarks
    img=detector.findHands(img)
    lmlist=detector.findPosition(img)

    if lmlist!=None and len(lmlist)>0:
        x1,y1=lmlist[8][1:]
        x2,y2=lmlist[12][1:]
    
   
          
    #3 check which fingers are up
    fingers= detector.fingerUp()
    
    #4 if selection mode -2 fingers are up 
    if fingers[0] and fingers[1]:
        xp=0
        yp=0
        cv2.rectangle(img,(x1-5,y1-30),(x2+5,y2+30 ),drawColor,cv2.FILLED)
        if y1<125:
            if 0<x1<208:
                header= overlayList[1]
                drawColor=(0,0,255)
            elif 209<x1<417:
                header= overlayList[2]
                drawColor=(255,0,255)
            elif 418<x1<627:
                header= overlayList[3]
                drawColor=(0,255,255)
            elif 628<x1<834:
                header= overlayList[4]
                drawColor=(0,255,0)
            elif 835<x1<1042:
                header= overlayList[5]
                drawColor=(203, 192, 255)
            else:
                header= overlayList[6]
                drawColor=(0,0,0)
    #5 if drawing mode =1 finger is up
    if fingers[0] and fingers[1]==False:
        cv2.circle(img, (x1,y1),15,drawColor,cv2.FILLED)
        if xp ==0 and yp==0:
            xp,yp=x1,y1
        
        if drawColor==(0,0,0):
            cv2.line(img,(xp,yp),(x1,y1),drawColor,25)
            cv2.line(imgCanvas,(xp,yp),(x1,y1),drawColor,25)
        else:
            cv2.line(img,(xp,yp),(x1,y1),drawColor,15)
            cv2.line(imgCanvas,(xp,yp),(x1,y1),drawColor,15)
        xp,yp=x1,y1
    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img,imgInv)
    img = cv2.bitwise_or(img,imgCanvas)        
    #setting the 
    img[0:150,0:1280]=header[50:200  ,:1280]
    # img=cv2.addWeighted(img,0.5,imgCanvas,0.5,0 )
    cv2.imshow("imageCanvas",imgCanvas)
    cv2.imshow("image",img)
    
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break