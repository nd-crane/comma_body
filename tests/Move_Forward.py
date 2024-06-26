
#!/usr/bin/env python3
import argparse

from bodyjim import BodyEnv

import pygame


def move_forward(env, distance, speed):
  duration = distance / abs(speed)
  action = [-speed,0]
  start_time = pygame.time.get_ticks()
  while (pygame.time.get_ticks() - start_time) < (duration * 1000):
    env.step(action)
    pygame.time.delay(100)
  
def run_forward_movement(body_ip, cameras, distance,speed):
  env = BodyEnv(body_ip, cameras,["accelerometer", "gyroscope", "gpsLocation"], render_mode="human")
  env.reset()
  env.render()
  move_forward(env, distance, speed)
  env.close()
  
if __name__ == "__main__":
    parser = argparse.ArgumentParser("Forward movement controller for the body")
    parser.add_argument("body_ip", help="IP address of the body")
    parser.add_argument("cameras", nargs="*", default=["driver"], help="List of cameras to render")
    parser.add_argument("--distance", type=float, default=1.0, help="Distance to move forward in inches")
    parser.add_argument("--speed", type=float, default=0.2, help="Speed of the movement (inches per second)")
    args = parser.parse_args()

    # Initialize pygame
    pygame.init()

    run_forward_movement(args.body_ip, args.cameras, args.distance, args.speed)
