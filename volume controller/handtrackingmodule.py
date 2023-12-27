import cv2 
import mediapipe as mp 
import time
import logging
logging.basicConfig()


class handDetector():
    def __init__(self , mode=False , maxHands=2  , complexity = 1, detectionCon=0.5 , trackCon=0.5):
        self.mode=mode
        self.maxHands=int(maxHands)  # Ensure maxHands is an integer
        self.detectionCon=detectionCon
        self.trackCon=trackCon
        
        self.mpHands=mp.solutions.hands
        self.complexity = complexity
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.complexity, self.detectionCon, self.trackCon)        
        self.mpdraw = mp.solutions.drawing_utils 
    
    def findhands(self , img , draw=True):
        imgRGB=cv2.cvtColor(img , cv2.COLOR_BGR2RGB) #converting the image to rgb because it only detects rgb images
        self.results = self.hands.process(imgRGB)
        #print(results.multi_hand_landmarks)
        if self.results.multi_hand_landmarks:
            for handlms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpdraw.draw_landmarks(img , handlms , self.mpHands.HAND_CONNECTIONS)
        return img
    
    
    
    def findPosition(self , img , handNo=0 ,draw=True ):
        lmlist=[]
        if self.results.multi_hand_landmarks:
            myhand = self.results.multi_hand_landmarks[handNo]
            for id , lm in enumerate(myhand.landmark):
                #print(id,lm)
                h , w , c = img.shape
                cx , cy = int(lm.x*w) , int(lm.y*h)
                lmlist.append([id , cx , cy])
                if draw:
                    cv2.circle(img , (cx,cy) , 15 , (255,0,259) , cv2.FILLED)
        return lmlist


def main():
    pTime=0
    cTime=0
    cap = cv2.VideoCapture(0)
    detector= handDetector()
    while True :
        success , img = cap.read()
        img = detector.findhands(img )
        lmlist = detector.findPosition(img)
        
        if len(lmlist)!=0:
            print(lmlist[4])
        cTime=time.time()
        fps=1/(cTime-pTime)
        pTime=cTime
            
        cv2.putText(img , str(int(fps)) , (10,70) , cv2.FONT_HERSHEY_COMPLEX , 3 , (255,0,255) , 3 )
        cv2.imshow("IMAGE" , img)
        #this loop is for the fps 
        #if we press escape the loop exits and the camera closes
        cv2.waitKey(1)


if __name__ == "__main__":
    main()