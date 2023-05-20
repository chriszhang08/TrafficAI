import pygame
import argparse
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import random

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Highway Simulation")

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)
gray = (100, 100, 100)
green = (116, 139, 117)
yellow = (255, 255, 0)
red = (255, 0, 0)

# Number of lanes
num_lanes = 3

# Highway properties
lane_width = 50
all_lanes_width = lane_width * num_lanes
lane_height = 600
lane_x = (width - all_lanes_width) // 2
lane_y = height - lane_height

# Road lines properties
line_width = 2
line_height = 10
line_gap = 10
num_lines = lane_height // (line_height + line_gap)

# Car properties
car_width = 15

# Car class
class Car:
    def __init__(self, x, y):
        # Randomly choose a lane
        self.x = x
        self.y = 0
        self.color = red
        self.car_radius = 15
        self.car_speed = random.randint(1, 5)

    def move(self):
        # TODO implement variable car speeds depending on conditions
        self.y += self.car_speed
        if self.y > height:
            self.car_radius = 0

    def brake(self):
        # gradually slow down
        while self.car_speed > 0:
            self.car_speed -= 1

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.car_radius)

# Create lanes
lanes = []
for i in range(num_lanes):
    lane_cars = []
    lanes.append(lane_cars)

# TODO create a function that takes an array of cars and returns how many cars are stopping
# TODO create a function that allows cars to change lanes

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(green)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw the highway
    pygame.draw.rect(screen, gray, (lane_x, lane_y, all_lanes_width, lane_height))

    # Draw the road lines if there is more than one lane
    for lane in range(num_lanes - 1):
        line_x = lane_x + (all_lanes_width - line_width) // num_lanes * (lane + 1)
        for i in range(num_lines):
            line_y = lane_y + i * (line_height + line_gap)
            pygame.draw.rect(screen, yellow, (line_x, line_y, line_width, line_height))

    # Spawn new cars randomly in each lane
    for i in range(num_lanes):
        if random.random() < 0.02:  # Adjust the probability as desired
            car_x = lane_x + (lane_width // 2) * (2 * i + 1)
            car_y = height
            new_car = Car(car_x, car_y)
            lanes[i].append(new_car)

    # Move and draw cars in each lane
    for lane_cars in lanes:
        for car in lane_cars:
            car.move()
            car.draw()
            if car.y > height:
                lane_cars.remove(car)

    pygame.display.update()
    clock.tick(60)

# Quit the game
pygame.quit()
