#!/Users/connerrauguth/Research/myenv/bin/python

import argparse
from bodyjim import BodyEnv
import pygame

# Global variables
BODY_IP = "10.12.54.125"
SPEED = 0.2
CAMERAS = ["driver"]

def move_forward(env, distance, speed):
    '''Function that controls the movement of the agent.'''
    # Determine duration of movement
    duration = distance / abs(speed)
    
    # Sets the action of the robot
    action = [-speed, 0]
    
    # Steps through movement via a while loop
    start_time = pygame.time.get_ticks()
    while (pygame.time.get_ticks() - start_time) < (duration * 1000):
        env.step(action)
        pygame.time.delay(100)

def run_forward_movement(body_ip, cameras, distance, speed):
    '''Function that will actually move the agent.'''
    # Creates the environment, which can track location and rotation
    env = BodyEnv(body_ip, cameras, ["accelerometer", "gyroscope", "gpsLocation"], render_mode="human")
    env.reset()
    env.render()
    
    # Calls the 'move function'
    move_forward(env, distance, speed)
    
    env.close()

def moveAv(distance):
    # Initialize pygame
    pygame.init()

    # Calls the function to actually move the agent
    run_forward_movement(BODY_IP, CAMERAS, distance, SPEED)


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Forward movement controller for the body")
    parser.add_argument("--distance", type=float, default=1.0, help="Distance to move forward in inches")
    args = parser.parse_args()

    # Sample input
    input = {'image': 1, 'circleFound': 1, 'distance': 1}
    
    # Move the agent
    if input['circleFound'] == 1:
        moveAv(input['distance'])
