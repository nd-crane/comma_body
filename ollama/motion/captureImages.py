#!/usr/bin/env python3

''' captureImages.py '''

import argparse
import os
from bodyjim import BodyEnv
import cv2
import pygame

# Global varibales
DIR = 'Pictures_From_Comma'
BODY_IP = '10.12.50.52'
CAMERAS = "wideRoad"

def captureFrames(env, DIR, interval, num_frames = 3):
    ''' Captures a specified number of images and saves them to a directory'''
    frame_count = 0
    while frame_count < num_frames:
        # Capture frame
        obs,_,_,_,_ = env.step([0,0])

        # Extract the frame from observations
        frame = obs["cameras"][CAMERAS]

        # Convert the frame from RGB to BGR (OpenCV format)
        frame = cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)

        # Save the frame as an image
        frame_path = os.path.join(DIR,f"frame_{frame_count:04d}.jpg")
        cv2.imwrite(frame_path,frame)

        # Wait before taking next frame
        pygame.time.delay(int(interval * 1000))
        frame_count += 1

def captureImages(interval):
    ''' Process of actualy capturing images on comma '''
    # Initilize pygame
    pygame.init()
    
    # Ensure the save directory exists
    if not os.path.exists(DIR):
        os.makedirs(DIR)
    
    # Initialize the body environment
    env = BodyEnv(BODY_IP, [CAMERAS], ["accelerometer", "gyroscope", "gpsLocation"], render_mode="human")
    env.reset()

    # Capture frames
    captureFrames(env, DIR, interval)
    
    env.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Frame capture from Comma Body video stream")
    parser.add_argument("--interval", type=float, default = 1.0, help = "Interval between frames in seconds")
    args = parser.parse_args()

    # Define time interval
    interval = 1

    captureImages(interval)
