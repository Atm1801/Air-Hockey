import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import random
import math



cap = cv2.VideoCapture(0)
cap.set(3, 920)
cap.set(4, 580)

imgBackground = cv2.imread("/Users/Atharv/Downloads/Resources/NewProject.png")
imgBall = cv2.imread("/Resources/imageok.png", cv2.IMREAD_UNCHANGED)
imgBat1 = cv2.imread("/Resources/Paddle_1.png", cv2.IMREAD_UNCHANGED)
imgBat2 = cv2.imread("/Resources/Paddle_2.png", cv2.IMREAD_UNCHANGED)
imggoal = cv2.imread("/Resources/gand.jpeg", cv2.IMREAD_UNCHANGED)
imgblue = cv2.imread("/Resources/bluewins.jpeg", cv2.IMREAD_UNCHANGED)
imgred = cv2.imread("/Resources/redwins.jpeg", cv2.IMREAD_UNCHANGED )

detector = HandDetector(detectionCon=0.8, maxHands=2)


ballPos = [1350, 480]
speedX = 0
speedY = 0
gameOver = False
score = [0,0]
isBallRight = 0
gameStop=1
collision=0


while True:
    _, img = cap.read()
    img = cv2.flip(img, 1)
    imgRaw = img.copy()


    hands,img = detector.findHands(img, flipType=False)


    img = cv2.addWeighted(img, 0.1, imgBackground, 0.9, 0)


    if hands:
        for hand in hands:
            x, y, w, h = hand['bbox']
            h1, w1, _ = imgBat1.shape
            y1 = (y - h1 // 2)*2
            x1 = np.clip(x,50,500)
            x2 = np.clip(x, 600, 1100)
            y1 = np.clip(y1, 5, 550)



            if hand['type'] == "Left":

                img = cvzone.overlayPNG(img, imgBat1, (x1, y1))
                if x1 < ballPos[0] < x1 + w1 and y1 - h1 < ballPos[1] < y1 + h1:
                    collision += 1
                    if abs(speedX)<=30:
                        speedX = -(speedX) - int(collision*math.copysign(0.35,speedX))
                    else:
                        speedX = -speedX
                    ballPos[0] += 20


            if hand['type'] == "Right":
                img = cvzone.overlayPNG(img, imgBat2, (x2, y1))
                if x2 - 50 < ballPos[0] < x2 and y1 -h1 < ballPos[1] < y1 + h1:
                    collision += 1
                    if abs(speedX)<=30:
                        speedX = -(speedX) - int(collision*math.copysign(0.35,speedX))
                    else:
                        speedX = -speedX
                    ballPos[0] -= 20

    if (0 < ballPos[1] < 190 or 480 < ballPos[1] < 640) and ballPos[0] < 20: #Red
        speedX = -speedX

    if (0 < ballPos[1] < 190 or 480 < ballPos[1] < 640) and ballPos[0] > 1180: #Blue
        speedX = -speedX


    if ballPos[0] < 50 and 190 < ballPos[1] <480 and not gameStop:
            isBallRight = 0
            score[1] = score[1] + 1
            gameStop=1
            ballPos = [1350, 480]
            speedX = 0
            speedY = 0
            img = cv2.addWeighted(img, 0.1, imggoal, 0.9, 0)
            cv2.imshow("Image", imggoal)


    elif ballPos[0] > 1180 and 190 < ballPos[1] < 480 and not gameStop:
            isBallRight = 1
            score[0] = score[0] + 1
            gameStop = 1
            ballPos = [1350, 480]
            speedX=0
            speedY=0
            img = cv2.addWeighted(img, 0.1, imggoal, 0.9, 0)
            cv2.imshow("Image", imggoal)


    if score[0]>=3 or score[1] >=3:
        gameStop=1
        gameOver=True
        if score[0] > score [1]:
            imgGameOver = cv2.imread("/Resources/redwins.jpeg", cv2.IMREAD_UNCHANGED)
        else:
            imgGameOver = cv2.imread("/Resources/bluewins.jpeg", cv2.IMREAD_UNCHANGED)

        img=imgGameOver


    else:


        if ballPos[1] >= 640 or ballPos[1] <= 50:
            speedY = -speedY

        ballPos[0] += speedX
        ballPos[1] += speedY

        img = cvzone.overlayPNG(img, imgBall, ballPos)

        cv2.putText(img, str(score[0]), (300, 650), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 255, 255), 5)
        cv2.putText(img, str(score[1]), (900, 650), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 255, 255), 5)


    cv2.imshow("Image", img)
    key = cv2.waitKey(2)
    if key == ord(' '):
        if isBallRight:
            ballPos = [550,random.randrange(2,640)]
            speedX = -15
            speedY = 15
        else:
            ballPos = [550, random.randrange(2, 640)]
            speedX = 15
            speedY = 15
        gameStop = 0


