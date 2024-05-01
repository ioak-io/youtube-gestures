import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import numpy as np
import math
import time
import pyautogui

cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=2)
classifier = Classifier('Model/keras_model.h5', 'Model/labels.txt')

offset = 20
imgSize = 300
counter = 0

labels = ["free_hand","right","left", "v_up","v_down","max","mlc","stop"]

control_delay = 1 # Delay in seconds before performing another control action
last_action_time = time.time() - control_delay

screenWidth, screenHeight = pyautogui.size()# Get screen resolution

while True:
    success, img = cap.read()
    imgOutput = img.copy()
    hands, img = detector.findHands(img)
    if hands:
        handCenters = []
        for hand in hands:
            x, y, w, h = hand['bbox']
            handCenterX = x + w // 2
            handCenterY = y + h // 2
            handCenters.append((handCenterX, handCenterY))

        # Calculate average position of both hands
        if len(handCenters) == 2:
            avgX = (handCenters[0][0] + handCenters[1][0]) // 2
            avgY = (handCenters[0][1] + handCenters[1][1]) // 2
            screenX = avgX / img.shape[1] * screenWidth
            screenY = avgY / img.shape[0] * screenHeight
            pyautogui.moveTo(screenX, screenY)

        for hand in hands:
            x, y, w, h = hand['bbox']
            imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
            imgCrop = img[y - offset: y + h + offset, x - offset: x + w + offset]

            if imgCrop.size == 0:
                print("Empty image crop. Skipping frame.")
                continue

            aspectRatio = h / w

            if aspectRatio > 1:
                k = imgSize / h
                wCal = math.ceil(k * w)
                imgResize = cv2.resize(imgCrop, (wCal, imgSize))
                imgResizeShape = imgResize.shape
                wGap = math.ceil((imgSize - wCal) / 2)
                imgWhite[:, wGap:wCal + wGap] = imgResize
                prediction, index = classifier.getPrediction(imgWhite, draw=True)
                print(prediction, ":", index)

            else:
                k = imgSize / w
                hCal = math.ceil(k * h)
                imgResize = cv2.resize(imgCrop, (imgSize, hCal))
                imgResizeShape = imgResize.shape
                hGap = math.ceil((imgSize - hCal) / 2)
                imgWhite[hGap:hCal + hGap, :] = imgResize
                prediction, index = classifier.getPrediction(imgWhite, draw=True)
                print(prediction, ":", index)

            cv2.rectangle(imgOutput, (x - offset, y - offset - 50), (x - offset + 90, y - offset - 50 + 50), (255, 0, 255),cv2.FILLED)
            cv2.putText(imgOutput, labels[index], (x, y - 20), cv2.FONT_HERSHEY_COMPLEX, 1.7, (255, 255, 255), 2)
            cv2.rectangle(imgOutput, (x - offset, y - offset), (x + w + offset, y + h + offset), (255, 0, 255), 4)

            cv2.imshow("ImageCrop", imgCrop)
            cv2.imshow("ImageWhite", imgWhite)

            current_time = time.time()

            if labels[index] == "v_up" :
                pyautogui.press("up") # Press up arrow key for volume up
                last_action_time = current_time
            elif labels[index] == "v_down":
                pyautogui.press("down") # Press down arrow key for volume down
                last_action_time = current_time
            elif labels[index] == "free_hand":
                handCenterX = x + w // 2
                handCenterY = y + h // 2
                screenX = handCenterX / img.shape[1] * screenWidth
                screenY = handCenterY / img.shape[0] * screenHeight
                pyautogui.moveTo(screenX, screenY) #mouse control
            elif labels[index] == "stop" and current_time - last_action_time >= control_delay:
                pyautogui.press("space") # Press spacebar to pause/play
                last_action_time = current_time
            elif labels[index] == "max" and current_time - last_action_time >= control_delay:
                pyautogui.press("f") # Press f to enter full screen
                last_action_time = current_time
            elif labels[index] == "mlc" and current_time - last_action_time >= control_delay:
                pyautogui.click() #left click
                last_action_time = current_time
            elif labels[index] == "right" and current_time - last_action_time >= control_delay:
                pyautogui.press("left") # Press Right Arrow to skip 5 sec
                last_action_time = current_time
            elif labels[index] == "left" and current_time - last_action_time >= control_delay:
                pyautogui.press("right") # Press Left Arrow to rewind 5 sec
                last_action_time = current_time   

    cv2.imshow("Image", imgOutput)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break