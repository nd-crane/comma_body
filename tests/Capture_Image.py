#!/usr/bin/env python3
import argparse
import os
from bodyjim import BodyEnv
import cv2
import numpy as np
import pygame

save_dir = 'Pictures_From_Comma'
body_ip = '10.12.1.88'
cameras = ["wideRoad"]
def Capture_and_Save_Frames(env, save_dir, interval, num_frames = 3):
    frame_count = 0
    while frame_count < num_frames:
        #Step the environment to get the next frame
        obs,_,_,_, info = env.step([0,0]) #No action, just capture the frame

        #Extract the frame from observations
        frame = obs["cameras"]["wideRoad"]

        #Convert the frame from RGB to BGR(OpenCV format)
        frame = cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)

        #Save the frame as an image
        frame_path = os.path.join(save_dir,f"frame_{frame_count:04d}.jpg")
        cv2.imwrite(frame_path,frame)

        #Wait for the specified interval
        pygame.time.delay(int(interval * 1000))
        frame_count += 1

def main(body_ip, cameras,save_dir,interval):
    #Ensure the save directory exists
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    #Initialize the body environment
    env = BodyEnv(body_ip, cameras, ["accelerometer", "gyroscope", "gpsLocation"], render_mode="human")
    env.reset()

    #Capture and Save Frames
    Capture_and_Save_Frames(env,save_dir,interval)
    env.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser("Frame capture from Comma Body video stream")
    parser.argparse.add_argument("--interval", type=float, default = 1.0, help = "Interval between frames in seconds")
    args = parser.parse_args()

    #initilize pygame
    pygame.init()

    main(save_dir,args.interval)