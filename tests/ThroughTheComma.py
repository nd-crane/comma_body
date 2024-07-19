import argparse
import os
from bodyjim import BodyEnv
import cv2
import pygame
import numpy as np
from ultralytics import YOLO
import time

class CommaBody:
    def __init__(self):
        self.heading = 0 #angle in radians
        self.model = YOLO('yolo-Weights/yolov8n.pt')

        bodyip = "10.12.64.77"
        mode = "rgb_array"


        self.env = BodyEnv(bodyip, ["wideRoad"], ["carState", "gyroscope"], render_mode=mode)
        self.obs, _ = self.env.reset()
        self.env.render()

        self.action = [-0.5,0.0]

        self.XPos = 0
        self.YPos = 0
        self.linearDist = 0

    def move(self, action):
        print(action["angle"])
        if abs(action["angle"]) > 0: #moves if there is an angle to move
            goal = self.heading + action["angle"]
            print(goal, self.heading)
            while abs(goal - self.heading) *(180/np.pi) >= .04180 * (180/np.pi):
                print(goal- self.heading)
                stepAct = (0, .7*((goal - self.heading)/abs(goal-self.heading)))
                LoopStartTime = time.perf_counter()
                self.env.step(stepAct)
                self.TelemetryUpdate(LoopStartTime)

        self.linearDist = 0 #sudo do while loop
        while action["distance"] >= self.linearDist: #only moves forward as of 7/10
            print (action["distance"], self.linearDist)
            LoopStartTime = time.perf_counter()
            stepAct = (-.7,0)
            self.env.step(stepAct)
            edge = self.ImageDetect(stepAct)
            self.TelemetryUpdate(LoopStartTime)
            if edge != 0 :
                print(edge)
                break
    def ImageDetect(self,stepAct):
        self.env.render()
        self.env.step(stepAct)
        img = self.obs["cameras"]["wideRoad"]

        DetectFrame = self.model(img, stream=True)

        # coordinates
        for r in DetectFrame:
            boxes = r.boxes

            for box in boxes:
                # bounding box
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) # convert to int values

                # put box in cam
                cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

        image = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)

        dst = cv2.Canny(image, 50, 60, None, 3)

        # Copy edges to the images that will display the results in BGR
        cdst = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR)
        cdstP = np.copy(cdst)

        # Probabilistic Line Transform
        linesP = cv2.HoughLinesP(dst, 1, np.pi / 180, 50, None, 50, 10)
        if linesP is not None:
            for i in range(0, len(linesP)):
                l = linesP[i][0]
                cv2.line(cdstP, (l[0], l[1]), (l[2], l[3]), (0,0,255), 3, cv2.LINE_AA)
        roi = (890, 1100, 178, 100)
        cdstpROI = cdstP[roi[1] : roi[1] + roi[3], roi[0] : roi[0] + roi[2]]

        lower_red0 = np.array([0,50,50])
        upper_red0 = np.array([10,255,255])

        lower_red1 = np.array([170,50,50])
        upper_red1 = np.array([180,255,255])

        hsv = cv2.cvtColor(cdstpROI, cv2.COLOR_BGR2HSV)
        mask0 = cv2.inRange(hsv, lower_red0, upper_red0)
        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask = mask0+mask1
        edge = np.sum(mask)
        return(edge)

    def TelemetryUpdate(self, LoopStartTime):
        movementTime = time.perf_counter() - LoopStartTime
        velocity = round(self.obs["carState"]["vEgo"],1)
        print(movementTime)
        self.XPos += np.sin(self.heading) * velocity * movementTime
        self.YPos += np.cos(self.heading) * velocity * movementTime
        self.linearDist += abs(velocity) * movementTime
        print(velocity, movementTime, self.linearDist)

        headingMod = (self.obs["gyroscope"]['gyroUncalibrated']['v'][0])
        if abs(headingMod) >= .3: self.heading += round(headingMod,1) * movementTime

    def MainRunLoop(self):
        while True:

            act = {"distance":0, "angle":0}
            act["distance"] = float(input("distance ->"))
            act["angle"] = float(input("angle ->")) * (np.pi/180)
            print(act)
            self.move(act)

CommaBody.MainRunLoop(CommaBody())
