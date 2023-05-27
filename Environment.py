import time

import pygame
import argparse
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import random

# Initialize Pygame
pygame.init()

# TODO reach goal calculate the carbon footprint wasted by sitting in traffic
# TODO calc the supply chain time wasted

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
button_color = (100, 100, 100)
hover = (66, 66, 66)

# Number of lanes
num_lanes = 3
num_merge_lanes = 1

# Highway properties
lane_height = 30
all_lanes_height = lane_height * num_lanes
lane_width = width
lane_x = width - lane_width
lane_y = (height - all_lanes_height) // 2

merge_lane_x = 200
merge_lane_y = lane_y + 100
exit_lane_x = 1200
exit_lane_y = lane_y + 100
# TODO make this variable and allow AI to control this
exit_ramp_width = 200

# Road lines properties
line_width = 10
line_height = 2
line_gap = 10
num_lines = lane_width // (line_height + line_gap)

lanes = []
spawn_timers = {}


def game_init():
    # TODO change the ramp width and entry/exit point
    # TODO change the number of lanes
    # TODO change the speed limit
    # Create lanes
    for i in range(num_lanes + num_merge_lanes):
        lane_cars = pygame.sprite.Group()
        lanes.append(lane_cars)

    # Create a global dictionary where the key is the lane number and the value is the spawn timer of that lane
    for i in range(num_lanes + num_merge_lanes):
        spawn_timers[i] = 0


# Button class
objects = []


# Button class
class Button:
    def __init__(self, x, y, text=""):
        self.rect = pygame.Rect(x, y, 50, 50)
        self.color = button_color
        self.hover_color = hover
        self.text_color = white
        self.text = text

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        text_surface = font.render(self.text, True, self.text_color)
        text_x = self.rect.centerx - text_surface.get_width() // 2
        text_y = self.rect.centery - text_surface.get_height() // 2
        surface.blit(text_surface, (text_x, text_y))

    def is_hover(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.color = self.hover_color
        else:
            self.color = button_color

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True

    def undraw(self):
        self.rect = pygame.Rect(0, 0, 0, 0)


class PlusButton(Button):
    def __init__(self, x, y):
        super().__init__(x, y)

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.rect.centerx, self.rect.centery), 25)
        pygame.draw.line(surface, self.text_color, (self.rect.centerx, self.rect.top + 10),
                         (self.rect.centerx, self.rect.bottom - 10), 5)
        pygame.draw.line(surface, self.text_color, (self.rect.left + 10, self.rect.centery),
                         (self.rect.right - 10, self.rect.centery), 5)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.increment_var()

    def increment_var(self):
        global num_lanes, all_lanes_height, lane_y
        num_lanes += 1
        all_lanes_height = lane_height * num_lanes
        lane_y = (height - all_lanes_height) // 2


class MinusButton(Button):
    def __init__(self, x, y):
        super().__init__(x, y)

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.rect.centerx, self.rect.centery), 25)
        pygame.draw.line(surface, self.text_color, (self.rect.left + 10, self.rect.centery),
                         (self.rect.right - 10, self.rect.centery), 5)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.decrement_var()

    def decrement_var(self):
        global num_lanes, all_lanes_height, lane_y
        if num_lanes > 1:
            num_lanes -= 1
            all_lanes_height = lane_height * num_lanes
            lane_y = (height - all_lanes_height) // 2


# Car class
class Car(pygame.sprite.Sprite):
    static_traffic_score = 0

    def __init__(self, x, y, lane):
        pygame.sprite.Sprite.__init__(self)
        # Randomly choose a lane
        self.x = 0
        self.y = y
        self.react_time = 0
        self.color = red
        self.car_radius = 5
        self.car_speed = 1
        self.braking_rate = .2
        self.origin = lane
        self.curr_lane = lane
        self.dest = 0
        if lane == 0:
            self.max_speed = 1.02
        elif lane == num_lanes - 1:
            self.max_speed = 0.8
        elif lane >= num_lanes:
            # TODO fix this so that the direction changes as well
            self.max_speed = 0.6
        else:
            self.max_speed = 0.95
        self.state = "cruising"

    def move(self, merge=False):
        # TODO implement variable car speeds depending on conditions
        if self.react_time > 0:
            self.react_time -= 1
        elif self.state == "braking":
            self.car_speed -= self.braking_rate
            if self.car_speed <= 0:
                self.car_speed = 0
                self.state = "stopped"
        elif self.state == "stopped":
            self.car_speed = 0
            Car.static_traffic_score += 1
        elif self.state == "cruising":
            self.car_speed = self.max_speed
        elif self.state == "accelerating":
            self.car_speed += .2
            if self.car_speed >= self.max_speed:
                self.car_speed = self.max_speed
                self.state = "cruising"
        self.x += self.car_speed
        if self.x > width:
            self.car_radius = 0

    # TODO change how fast cars accelerate and brake depending on the state
    def brake(self, car_distance):
        # gradually slow down
        self.state = "braking"
        if self.react_time == 0:
            self.react_time = 2
        if car_distance < 5:
            self.braking_rate = 1
        # TODO change the braking rate depending on the distance between cars
        elif car_distance < 20:
            self.braking_rate = .2
        elif car_distance == 0:
            self.react_time = 0
            self.braking_rate = .2
        else:
            self.braking_rate = .01

    def accelerate(self):
        # gradually speed up
        self.state = "accelerating"

    # TODO configure the reaction times to be dependent on the state of the car
    def react(self, sleep_time=0):
        # react to the car in front of you
        self.react_time = sleep_time

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.car_radius)


# TODO create a function that takes a pygame Group of Cars and changes their states so that
# they accelerate if there is space in front of them, brake if they are too close to the car in front of them,
# and stop if they are at the end of the highway
def update_car_states(cars):
    list_of_cars = cars.sprites()
    if list_of_cars[0].state == "stopped":
        list_of_cars[0].react(20)
        list_of_cars[0].accelerate()
    for i in range(1, len(list_of_cars)):
        # brake if the car in front of them is too close
        if list_of_cars[i - 1].x - list_of_cars[i].x < 20 and list_of_cars[i].state != "braking":
            list_of_cars[i].brake(list_of_cars[i - 1].x - list_of_cars[i].x)
        # accelerate if there is space in front of them
        elif ((list_of_cars[i - 1].x - list_of_cars[i].x > 30) and
              (list_of_cars[i].state == "stopped" or list_of_cars[i].state == "braking")):
            list_of_cars[i].react(2)
            list_of_cars[i].accelerate()


# Spawn new cars randomly in each lane
# Change the spawn timer and random number to adjust the frequency of car spawns
def spawn_cars():
    PROBABILITY = 1
    # Create a car
    spawn_lane = random.randint(0, num_lanes + num_merge_lanes - 1)

    if spawn_timers[spawn_lane] <= 0:
        car_x = 0
        car_y = lane_y + (lane_height // 2) * (2 * spawn_lane + 1)
        new_car = Car(car_x, car_y, spawn_lane)
        lanes[spawn_lane].add(new_car)
        if spawn_lane == 0:
            spawn_timers[spawn_lane] = random.randint(40, 70)
        elif spawn_lane == num_lanes - num_merge_lanes - 1:
            spawn_timers[spawn_lane] = random.randint(30, 40)
        elif spawn_lane >= num_lanes:
            spawn_timers[spawn_lane] = random.randint(70, 80)
        else:
            spawn_timers[spawn_lane] = random.randint(35, 65)
    # decrement the spawn timer
    for i in range(num_lanes + num_merge_lanes):
        spawn_timers[i] -= 1


# return the coordinates of the points of the polygon that represents the ramp
def draw_ramp(ramp_x, ramp_y, exit_or_merge):
    if exit_or_merge == "merge":
        # create 2 similar triangles
        ramp_rect_coords = (
            (ramp_x, lane_y + all_lanes_height),
            (ramp_x, lane_y + all_lanes_height + lane_height),
            (0, ramp_y + lane_height),
            (0, ramp_y)
        )
        ramp_merge_coords = (
            (ramp_x, lane_y + all_lanes_height),
            (ramp_x + exit_ramp_width, lane_y + all_lanes_height),
            (ramp_x, lane_y + all_lanes_height + lane_height)
        )
    else:
        ramp_rect_coords = (
            (ramp_x, lane_y + all_lanes_height),
            (ramp_x, lane_y + all_lanes_height + lane_height),
            (width, ramp_y + lane_height),
            (width, ramp_y)
        )
        ramp_merge_coords = (
            (ramp_x, lane_y + all_lanes_height),
            (ramp_x - exit_ramp_width, lane_y + all_lanes_height),
            (ramp_x, lane_y + all_lanes_height + lane_height)
        )
    pygame.draw.polygon(screen, gray, ramp_rect_coords)
    pygame.draw.polygon(screen, gray, ramp_merge_coords)


# TODO create a function that allows cars to change lanes

# Game loop
running = True
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)  # You can specify the font file and size

counter = 0
game_set = False

def add_road():
    global num_lines
    num_lines += 1

def remove_road():
    global num_lines
    num_lines -= 1


while running and counter < 100:
    screen.fill(green)

    plus_button = PlusButton(1250, 30)
    minus_button = MinusButton(1100, 30)
    set_button = Button(675, 500, "Go")

    plus_button.is_hover()
    minus_button.is_hover()
    set_button.is_hover()
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if set_button.handle_event(event):
            game_init()
            set_button.undraw()
            game_set = True
        plus_button.handle_event(event)
        minus_button.handle_event(event)

    plus_button.draw(screen)
    minus_button.draw(screen)
    if not game_set:
        set_button.draw(screen)

    # Draw the highway
    pygame.draw.rect(screen, gray, (lane_x, lane_y, lane_width, all_lanes_height))
    # TODO exit lane and merge lane slider and toggle button
    # TODO form for how many arterial lanes
    draw_ramp(merge_lane_x, merge_lane_y, exit_or_merge="merge")
    draw_ramp(exit_lane_x, exit_lane_y, exit_or_merge="exit")

    # Draw the road lines if there is more than one lane
    for lane in range(num_lanes - 1):
        line_y = lane_y + (all_lanes_height - line_height) // num_lanes * (lane + 1)
        for i in range(num_lines):
            line_x = lane_x + i * (line_height + line_gap)
            pygame.draw.rect(screen, yellow, (line_x, line_y, line_width, line_height))

    # Show the traffic score
    traffic_score = Car.static_traffic_score
    traffic_score_text = font.render("Traffic Score: " + str(traffic_score), True, black)
    screen.blit(traffic_score_text, (10, 10))
    counter_text = font.render("Counter: " + str(counter), True, black)
    screen.blit(counter_text, (10, 30))
    roads_text = font.render("No. of Roads", True, black)
    screen.blit(roads_text, (400, 30))
    for object in objects:
        object.process()

    # Spawn cars
    if game_set:
        spawn_cars()

    # Move and draw cars in each lane
    for lane_cars in lanes:
        for car in lane_cars:
            update_car_states(lane_cars)
            car.move()
            car.draw()
            if car.x > width:
                car.kill()
                counter += 1

    pygame.display.update()
    clock.tick(60)

# Quit the game
pygame.quit()
