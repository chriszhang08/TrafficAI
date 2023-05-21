import pygame
import argparse
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import random

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 800
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
num_lanes = 1

# Highway properties
lane_width = 50
all_lanes_width = lane_width * num_lanes
lane_height = height
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
class Car(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        # Randomly choose a lane
        self.x = x
        self.y = 0
        self.react_time = 0
        self.color = red
        self.car_radius = 15
        self.car_speed = random.randint(4, 5)
        # TODO implement car state (accelerating, braking, stopped, etc.)
        self.state = "cruising"

    def move(self):
        # TODO implement variable car speeds depending on conditions
        if (self.react_time > 0):
            self.react_time -= 1
        elif (self.state == "braking"):
            self.car_speed -= .2
            if (self.car_speed <= 0):
                self.car_speed = 0
                self.state = "stopped"
        elif (self.state == "stopped"):
            self.car_speed = 0
        elif (self.state == "cruising"):
            self.car_speed = 5
        elif (self.state == "accelerating"):
            self.car_speed += .2
            if (self.car_speed >= 5):
                self.car_speed = 5
                self.state = "cruising"
        self.y += self.car_speed
        if self.y > height:
            self.car_radius = 0

    # TODO change how fast cars accelerate and brake depending on the state
    def brake(self):
        # gradually slow down
        self.state = "braking"

    def accelerate(self):
        # gradually speed up
        self.state = "accelerating"

    # TODO configure the reaction times to be dependent on the state of the car
    def react(self):
        # react to the car in front of you
        self.react_time = 20

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.car_radius)


# Create lanes
lanes = []
for i in range(num_lanes):
    lane_cars = pygame.sprite.Group()
    lanes.append(lane_cars)


# TODO create a function that takes a pygame Group of Cars and changes their states so that
# they accelerate if there is space in front of them, brake if they are too close to the car in front of them,
# and stop if they are at the end of the highway
def update_car_states(cars):
    list_of_cars = cars.sprites()
    for i in range(1, len(list_of_cars)):
        if ((list_of_cars[i-1].y - list_of_cars[i].y < 100) and
                (list_of_cars[i-1].state == "braking" or list_of_cars[i-1].state == "stopped")):
            list_of_cars[i].brake()
        elif ((list_of_cars[i-1].y - list_of_cars[i].y > 100) and
              (list_of_cars[i].state == "stopped" or list_of_cars[i].state == "braking")):
            list_of_cars[i].accelerate()

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
            lanes[i].add(new_car)

    # Move and draw cars in each lane
    for lane_cars in lanes:
        for car in lane_cars:
            update_car_states(lane_cars)
            car.move()
            car.draw()
            if car.y > height:
                car.kill()
            if car.y == height - 400 and car.car_speed > 0:
                car.brake()
            if car.state == "stopped":
                car.react()
                car.accelerate()

    pygame.display.update()
    clock.tick(60)

# Quit the game
pygame.quit()
