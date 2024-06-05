#!/usr/bin/env python3

''' moveAv.py '''

import argparse
from bodyjim import BodyEnv
import pygame

# Global variables
BODY_IP = "10.12.54.125"
SPEED = 0.5
CAMERAS = ["driver"]

def move_forward(env, distance, speed):
    ''' Controls the movement of the agent '''
    # Determine duration of movement
    duration = distance / abs(speed)
    
    # Sets the action of the robot
    action = [-speed, 0]
    
    # Steps through movement via a while loop
    start_time = pygame.time.get_ticks()
    while (pygame.time.get_ticks() - start_time) < (duration * 1000):
        env.step(action)
        # pygame.time.delay(100)

def moveAv(distance):
    ''' Process of actaully moving the comma '''
    # Initialize pygame
    pygame.init()
    
    # Creates the environment, which can track location and rotation
    env = BodyEnv(BODY_IP, CAMERAS, ["accelerometer", "gyroscope", "gpsLocation"], render_mode="human")
    env.reset()
    env.render()
    
    # Moves the robot
    move_forward(env, distance, SPEED)
    
    env.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Forward movement controller for the body")
    parser.add_argument("--distance", type=float, default=1.0, help="Distance to move forward in inches")
    args = parser.parse_args()

    # Get motion recommendation from LLM
    input = {'image': 1, 'circleFound': 1, 'distance': 1}
    
    # Move the agent if circle is found
    if input['circleFound'] == 1:
        moveAv(input['distance'])
