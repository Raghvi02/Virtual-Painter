import cv2
import mediapipe as mp

class Detector():
    def __init__(self,mode=False, maxHands=2,detectionconf= 0.5, trackconf=0.5):
        self.mode=mode
        self.maxHands= maxHands
        self.detectioncon=detectionconf
        self.trackingcon= trackconf
        self.mpHands= mp.solutions.hands
        self.hands= self.mpHands.Hands()
        self.mpDraw= mp.solutions.drawing_utils
        self.tipsIds=[4,8,12,16,20]
    def findHands(self,img,draw=True):
        imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results=self.hands.process(imgRGB) 
        if self.results.multi_hand_landmarks:
            for handLMS in self.results.multi_hand_landmarks:
                if draw: 
                    self.mpDraw.draw_landmarks(img,handLMS,self.mpHands.HAND_CONNECTIONS)    
        return img 
    def findPosition(self, img, handNo=0):
      
        self.lmList = []    
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
            
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
            
                self.lmList.append([id, cx, cy])
                
        return self.lmList

    
    
    
    def fingerUp(self):   
        fingers=[]
        
        # if self.lmList!=None and len(self.lmList)>0 and (self.lmList[self.tipsIds[0]][1]>self.lmList[self.tipsIds[0]-1][1]):
        #     fingers.append(1)
        # else:
        #     fingers.append(0)
        for id in range(1,3):
            if self.lmList!=None and len(self.lmList)>0 and (self.lmList[self.tipsIds[id]][2]<self.lmList[self.tipsIds[id]-2][2]):
                fingers.append(1)
            else:
                fingers.append(0)   
        return fingers   
                           
# cap = cv2.VideoCapture(0)
# detector= Detector()     
# while True:
#     success, img = cap.read()
#     #print(success)
#     img =detector.findHands(img)
#     fingers=detector.findpos(img,0)
#     # fingers=detector.fingersUp()
#     print(fingers)
#     cv2.imshow("Image", img)
   
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
