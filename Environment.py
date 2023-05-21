import pygame
import argparse
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import random

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 1400, 600
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
lane_height = 50
all_lanes_height = lane_height * num_lanes
lane_width = width
lane_x = width - lane_width
lane_y = (height - all_lanes_height) // 2

# Road lines properties
line_width = 10
line_height = 2
line_gap = 10
num_lines = lane_width // (line_height + line_gap)

# Car properties
car_width = 10

# Car class
class Car(pygame.sprite.Sprite):
    static_traffic_score = 0
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        # Randomly choose a lane
        self.x = 0
        self.y = y
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
            Car.static_traffic_score += 0.5
            if (self.car_speed <= 0):
                self.car_speed = 0
                self.state = "stopped"
        elif (self.state == "stopped"):
            self.car_speed = 0
            Car.static_traffic_score += 1
        elif (self.state == "cruising"):
            self.car_speed = 5
        elif (self.state == "accelerating"):
            self.car_speed += .2
            if (self.car_speed >= 5):
                self.car_speed = 5
                self.state = "cruising"
        self.x += self.car_speed
        if self.x > width:
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
font = pygame.font.Font(None, 36)  # You can specify the font file and size
spawn_timer = 0

counter = 0
while running and counter < 1000:
    screen.fill(green)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw the highway
    pygame.draw.rect(screen, gray, (lane_x, lane_y, lane_width, all_lanes_height))

    # Draw the road lines if there is more than one lane
    for lane in range(num_lanes - 1):
        line_y = lane_y + (all_lanes_height - line_width) // num_lanes * (lane + 1)
        for i in range(num_lines):
            line_x = lane_x + i * (line_height + line_gap)
            pygame.draw.rect(screen, yellow, (line_x, line_y, line_width, line_height))

    # Show the traffic score
    traffic_score = Car.static_traffic_score
    traffic_score_text = font.render("Traffic Score: " + str(traffic_score), True, black)
    screen.blit(traffic_score_text, (10, 10))
    counter_text = font.render("Counter: " + str(counter), True, black)
    screen.blit(counter_text, (10, 30))

    # Spawn new cars randomly in each lane
    # Change the spawn timer and random number to adjust the frequency of car spawns
    SPAWN_DELAY = 8
    PROBABILITY = 0.2
    for i in range(num_lanes):
        if spawn_timer > 0:
            spawn_timer -= 1
        if random.random() < PROBABILITY and spawn_timer == 0:  # Adjust the probability as desired
            car_x = 0
            car_y = lane_y + (lane_height // 2) * (2 * i + 1)
            new_car = Car(car_x, car_y)
            lanes[i].add(new_car)
            spawn_timer = SPAWN_DELAY

    # Move and draw cars in each lane
    for lane_cars in lanes:
        for car in lane_cars:
            update_car_states(lane_cars)
            car.move()
            car.draw()
            if car.x > width:
                car.kill()
                counter += 1
            if car.x == width - 400 and car.car_speed > 0:
                car.brake()
            if car.state == "stopped":
                car.react()
                car.accelerate()

    pygame.display.update()
    clock.tick(60)

# Quit the game
pygame.quit()
