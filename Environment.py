import time
import pygame
import argparse
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import random
import copy
from enum import Enum

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
slider_color = (200, 200, 200)
slider_handle_color = (150, 150, 150)

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
merge_lane_y = lane_y + 120
exit_lane_x = 1200
exit_lane_y = lane_y + 120
exit_ramp_width = 200

# Define slider properties
slider_width = 300
slider_height = 20

# Define handle properties
handle_width = 20
handle_height = slider_height + 10

# Define value range
min_value = 50
max_value = 400

# Road lines properties
line_width = 10
line_height = 2
line_gap = 10
num_lines = lane_width // (line_height + line_gap)

class CarState(Enum):
    MERGING = 0
    STOPPED = 1
    BRAKING = 2
    CRUISING = 3
    ACCELERATING = 4

class Merging(Enum):
    NO_MERGE = 0
    BEGAN_MERGE = 1
    MERGE_IN_PROGRESS = 2
    MERGING_FINISHED = 3  # if merging has finished, then another car can merge
                          # (we will have merging limit set to 1 at a time)

currently_merging = False

lanes = []
spawn_timers = {}


def game_init():
    # TODO change the speed limit
    # Create lanes
    for i in range(num_lanes + num_merge_lanes):
        lane_cars = pygame.sprite.Group()
        lanes.append(lane_cars)

    # Create a global dictionary where the key is the lane number and the value is the spawn timer of that lane
    for i in range(num_lanes + num_merge_lanes):
        spawn_timers[i] = 0


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
        global num_lanes, all_lanes_height, lane_y, exit_lane_y, merge_lane_y
        if num_lanes < 12:
            num_lanes += 1
            all_lanes_height = lane_height * num_lanes
            lane_y = (height - all_lanes_height) // 2
            exit_lane_y += lane_height // 2
            merge_lane_y += lane_height // 2


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
        global num_lanes, all_lanes_height, lane_y, merge_lane_y, exit_lane_y
        if num_lanes > 1:
            num_lanes -= 1
            all_lanes_height = lane_height * num_lanes
            lane_y = (height - all_lanes_height) // 2
            exit_lane_y -= lane_height // 2
            merge_lane_y -= lane_height // 2


# Slider class
class Slider:
    def __init__(self, x, y, width, height, handle_width, handle_height, color, handle_color):
        global exit_ramp_width
        self.rect = pygame.Rect(x, y, width, height)
        self.handle_rect = pygame.Rect(x, y - (handle_height - height) // 2, handle_width, handle_height)
        self.color = color
        self.handle_color = handle_color
        self.dragging = False
        self.handle_rect.centerx = exit_ramp_width + self.rect.left

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, self.handle_color, self.handle_rect)

    def handle_event(self, event):
        global exit_ramp_width
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.handle_rect.collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.handle_rect.centerx = event.pos[0]
                if self.handle_rect.left < self.rect.left:
                    self.handle_rect.left = self.rect.left
                elif self.handle_rect.right > self.rect.right:
                    self.handle_rect.right = self.rect.right

                # Update value based on position
                offset = self.handle_rect.centerx - self.rect.left
                exit_ramp_width = int(offset) + min_value


class Ramp():
    def __init__(self, x, y, exit_or_merge):
        self.ramp_x = x
        self.ramp_y = y
        self.color = gray
        self.hover_color = hover
        self.exit_or_merge = exit_or_merge
        self.dragging = False
        if exit_or_merge == "merge":
            self.drag_box = pygame.Rect(self.ramp_x - 50, lane_y + all_lanes_height, exit_ramp_width + 100,
                                        lane_height * 3)
        else:
            self.drag_box = pygame.Rect(self.ramp_x - exit_ramp_width - 50, lane_y + all_lanes_height,
                                        exit_ramp_width + 100, lane_height * 3)

    def is_hovered(self):
        if self.drag_box.collidepoint(pygame.mouse.get_pos()):
            self.color = self.hover_color
        else:
            self.color = gray

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.drag_box.collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.ramp_x = event.pos[0] + 10
                if self.drag_box.left < 50:
                    self.drag_box.left = 50
                elif self.drag_box.right > width - 50:
                    self.drag_box.right = width - 50

    # return the coordinates of the points of the polygon that represents the ramp
    def draw(self, surface):
        if self.exit_or_merge == "merge":
            # create 2 similar triangles
            ramp_rect_coords = (
                (self.ramp_x, lane_y + all_lanes_height),
                (self.ramp_x, lane_y + all_lanes_height + lane_height),
                (0, self.ramp_y + lane_height),
                (0, self.ramp_y)
            )
            ramp_lane_coords = (
                (self.ramp_x, lane_y + all_lanes_height),
                (self.ramp_x, lane_y + all_lanes_height + lane_height),
                (self.ramp_x + exit_ramp_width, lane_y + all_lanes_height + lane_height - 8),
                (self.ramp_x + exit_ramp_width, lane_y + all_lanes_height)
            )
            ramp_merge_coords = (
                (self.ramp_x + exit_ramp_width, lane_y + all_lanes_height),
                (self.ramp_x + exit_ramp_width + 50, lane_y + all_lanes_height),
                (self.ramp_x + exit_ramp_width, lane_y + all_lanes_height + lane_height - 8)
            )
        else:
            ramp_rect_coords = (
                (self.ramp_x, lane_y + all_lanes_height),
                (self.ramp_x, lane_y + all_lanes_height + lane_height),
                (width, self.ramp_y + lane_height),
                (width, self.ramp_y)
            )
            ramp_lane_coords = (
                (self.ramp_x, lane_y + all_lanes_height),
                (self.ramp_x, lane_y + all_lanes_height + lane_height),
                (self.ramp_x - exit_ramp_width, lane_y + all_lanes_height + lane_height - 8),
                (self.ramp_x - exit_ramp_width, lane_y + all_lanes_height)
            )
            ramp_merge_coords = (
                (self.ramp_x - exit_ramp_width, lane_y + all_lanes_height),
                (self.ramp_x - exit_ramp_width - 50, lane_y + all_lanes_height),
                (self.ramp_x - exit_ramp_width, lane_y + all_lanes_height + lane_height - 8)
            )
        pygame.draw.polygon(surface, self.color, ramp_rect_coords)
        pygame.draw.polygon(surface, self.color, ramp_lane_coords)
        pygame.draw.polygon(surface, self.color, ramp_merge_coords)


# TODO: mark car ahead as "merged" using Enum; have car_behind speed up; have variable speeds, accelerate until distance between cars is zero
# need to keep track of cars on the left, right, and middle... and determine the gap between each car so that you know the WINDOW on the right
# have to add that Sprite to the lane_cars for the other lane upon merging
# need to know if merging into the left or right lane
# CONSTRAINT: can only have 1 car merge at a time
# and left
# randomly have cars merge
# make merging more customizable
# if car_ahead merges, then speed up

# Lane class
class Lane(pygame.sprite.Sprite):
    static_lane_number = 0
    # access to the lane_cars for all the lanes (2D array)
    static_lane_cars = []  # list of pygame.sprite.Group objects
    static_distance_windows = []  # list of all distance windows for each lane
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.lane_number = Lane.static_lane_number
        Lane.static_lane_number += 1
        self.lane_cars = pygame.sprite.Group()  # maybe delete
        self.lane_cars_list = []  # includes merged-in cars
        Lane.static_lane_cars.append(self.lane_cars_list)
        self.distance_windows = []
        Lane.static_distance_windows.append(self.distance_windows)

    # TODO create a function that takes a pygame Group of Cars and changes their states so that
    # they accelerate if there is space in front of them, brake if they are too close to the car in front of them,
    # and stop if they are at the end of the highway
    def update_car_states(self, list_of_cars):
        # list_of_cars = cars.sprites()
        if list_of_cars[0].state == CarState.STOPPED:
            list_of_cars[0].react(20)
            list_of_cars[0].accelerate()
        for i in range(1, len(list_of_cars)):
            # brake if the car in front of them is too close
            if list_of_cars[i - 1].x - list_of_cars[i].x < 20 and list_of_cars[i].state != CarState.BRAKING:
                list_of_cars[i].brake(list_of_cars[i - 1].x - list_of_cars[i].x)
            # accelerate if there is space in front of them
            elif ((list_of_cars[i - 1].x - list_of_cars[i].x > 30) and
                  (list_of_cars[i].state == CarState.STOPPED or list_of_cars[i].state == CarState.BRAKING)):
                list_of_cars[i].react(2)
                list_of_cars[i].accelerate()

        # calculate windows between cars
        self.calculate_window()

    def update_lane_cars_list(self, new_list):
        self.lane_cars_list = new_list

    def add(self, car, is_merged=False, merge_idx=None):
        # self.lane_cars.add(car)
        # new_group = pygame.sprite.Group()
        # idx = 0
        # for a_car in self.lane_cars.sprites():
        #     if idx == merge_idx:
        #         new_group.add(car)
        #     else:
        #         new_group.add(a_car)
        #     idx += 1
        #
        # self.lane_cars = new_group

        if is_merged:
            self.lane_cars_list.insert(merge_idx, car)
        if not is_merged:
            self.lane_cars_list.append(car)

    def switch_lanes(self, new_lane, car, former_idx, new_index):
        new_lane.add(car, True, new_index)
        # TODO: commenting out the line below allows all cars to move in each lane
        # new_lane.update_lane_cars_list(new_lane.lane_cars_list[:new_index] + [car] + new_lane.lane_cars_list[new_index:])
        # remove car from THIS (current) Sprite group
        # update the car's lane number
        car.lane_number = new_lane.lane_number
        self.lane_cars_list.pop(former_idx)
        # self.lane_cars.remove(car)
        print("car state in switch_lanes: ", car.state)
        print("car merge in switch_lanes: ", Car.merging_state)

    def display(self):
        # car_ahead = None
        global currently_merging, counter
        print("")
        currently_merging = False
        for idx, car in enumerate(self.lane_cars_list):
            if idx > 0 and self.lane_cars_list:
                car.update_car_ahead(self.lane_cars_list[idx - 1])
            self.update_car_states(self.lane_cars_list)
            # if idx > 0 and ((car.state == CarState.MERGING) or car.merge(self.lane_cars_list[idx - 1])):
            car.move()
            print("curr merge: ", currently_merging)
            if currently_merging and car.state == CarState.MERGING:
                print("working correctly")
            if currently_merging and car.state == CarState.MERGING:
                print(f"car {car} can be merged")
            if not currently_merging:
               car.merge(self.lane_cars_list[idx - 1])
            car.draw()
            if car.x > width:
                car.kill()
                counter += 1
            if car.x == 600:
                car.brake(0)

            # car_ahead = car

    @property
    def distance_window_list(self):
        return self.distance_windows

    def calculate_window(self):
        """Keep calculating windows from car_ahead and car_behind to determine ideal merging time."""
        # list_of_cars = self.lane_cars.sprites()
        car_ahead_idx = 0
        self.distance_windows.clear()  # clear the distance windows upon each recalculation
        for idx in range(1, len(self.lane_cars_list) - 1):
            # start at the second car since there is no car_ahead for the first car
            # keep track of current car idx and insert car into there for that lane
            # curr_location = list_of_cars[idx].location
            # this_location = list_of_cars[car_ahead_idx].location
            # this_window = abs(curr_location - this_location)
            this_window = self.lane_cars_list[idx].distance(self.lane_cars_list[car_ahead_idx])
            self.distance_windows.append(this_window)
            car_ahead_idx = idx

# Create a global dictionary where the key is the lane number and the value is the spawn timer of that lane
spawn_timers = {}
for i in range(num_lanes):
    spawn_timers[i] = 0


# Car class
class Car(pygame.sprite.Sprite):
    static_traffic_score = 0
    static_car_id = 0
    merging_state = Merging.NO_MERGE
    merge_count = 0
    def __init__(self, x, y, lane_number):
        pygame.sprite.Sprite.__init__(self)

        # identifying cars
        self.static_id = Car.static_car_id
        Car.static_car_id += 1

        self.x = 0
        self.y = y
        self.lane_number = lane_number
        self.react_time = 0
        self.color = red
        self.car_radius = 5
        self.car_speed = 1
        self.braking_rate = .2
        self.car_speed = 0
        self.merging_direction = None
        self.car_ahead = None  # modify this value when car merges; update this value each time we call move()
        # TODO implement car state (accelerating, braking, stopped, etc.)
        self.state = CarState.CRUISING
        # merging attributes
        self.merging_lane = None
        self.car_index = None
        self.merging_index = None

    def move(self):
    # TODO implement variable car speeds depending on conditions
        if (self.react_time > 0):
            self.react_time -= 1
        elif (self.state == CarState.MERGING):
            # TODO: never gets here
            print("is in move MERGING")
            self.car_speed += .4
            Car.merging_state == Merging.MERGE_IN_PROGRESS
            self.state = CarState.MERGING
            self.continue_merge()
        elif (self.state == CarState.BRAKING):
            self.car_speed -= self.braking_rate
            if self.car_speed <= 0:
                self.car_speed = 0
                self.state = CarState.STOPPED
        elif (self.state == CarState.STOPPED):
            self.car_speed = 0
            Car.static_traffic_score += 1
        elif (self.state == CarState.CRUISING):
            # this is where the merging happens
            # if merge:
            #     print("in cruising for merge")
            #     self.state = CarState.MERGING
            # TODO: should there be an "else" here?
            # self.car_speed = 1
            temp_car_speed = random.randrange(0, 2)
            # pick a speed that won't get you to run into the car in front
            if self.car_ahead is not None:
                potential_x = self.x + temp_car_speed
                max_potential_x = self.car_ahead.x - 10 - self.car_radius
                # find speed at which there is ample distance between current car & car ahead
                while potential_x >= max_potential_x:
                    temp_car_speed = random.randrange(0, 2)
            self.car_speed = temp_car_speed
        # elif (self.state == CarState.MERGING):
        #     # TODO: NEVER GETS HERE
        #     print("in merge")
        #     # Car.merging_state = Merging.BEGAN_MERGE
        #     self.car_speed += .4
        #     self.continue_merge()
        elif (self.state == CarState.ACCELERATING):
            self.car_speed += .2
            if (self.car_speed >= 1):
                self.car_speed = 1
                self.state = CarState.CRUISING
        self.x += self.car_speed
        if self.x > width:
            self.car_radius = 0
        print("MERGECNT: ", Car.merge_count)
        if Car.merge_count <= 5:
            print("reseting to cruising state")
            self.state = CarState.CRUISING
            Car.merge_count = 0
            self.merging_state = Merging.NO_MERGE

    def update_car_ahead(self, car_ahead):
        self.car_ahead = car_ahead
    @property
    def location(self):
        return self.x

    # @property
    def merge(self, car_ahead):
        """
        Determine conditions for which to merge. (i.e. closed lanes, cars, surroundings, etc)
        """
        # other factors: need to know which lane car is currently in to determine
        # if there is a car in the nearby lanes that will be in the way when attempting to merge
        # car ahead is stopping traffic, switch lanes
        global lanes, currently_merging

        if currently_merging:
            return False

        if self.state == CarState.MERGING and Car.merging_state == Merging.MERGE_IN_PROGRESS:
            return True

        if not car_ahead or (Car.merging_state == Merging.MERGE_IN_PROGRESS and self.state != CarState.MERGING):
            return False

        # car_ahead_influence = (car_ahead.state == CarState.BRAKING or car_ahead.state == CarState.STOPPED or \
                              # self.distance(car_ahead) < 1)
        # car from behind is too close, want to switch lanes
        # car_behind_influence = car_behind.state == "accelerating" and self.distance(car_behind) < 10
        # determine when merge will happen
        merge_value = self.initiate_merge()
        if merge_value:
            Car.merging_state = Merging.MERGE_IN_PROGRESS
            return True

        return False

    @property
    def speed(self):
        return self.car_speed

    def distance(self, car_other):
        return abs(self.x - car_other.x)

    def initiate_merge(self):
        global lanes
        global currently_merging

        if Car.merging_state == Merging.MERGE_IN_PROGRESS and self.state != CarState.MERGING:
            return False

        print("can merge with status", Car.merging_state)
        if not Car.merging_state == Merging.MERGE_IN_PROGRESS:  # do step 1, 2
            # 1. check left & right windows from left & right lanes; must look at the NEARBY windows to merge, NOT
            # just the leftmost or rightmost because cars driving at diff speeds
            # check these windows: left, left - 1, left + 1; right, right - 1, right + 1
            # TODO: ONLY DO THIS CHECK ONCE PER MERGE
            lane_left = None
            lane_right = None
            if self.lane_number > 0:
                lane_left = lanes[self.lane_number - 1]
            if self.lane_number < len(lanes) - 1:
                lane_right = lanes[self.lane_number + 1]

            if not lane_left and not lane_right:
                return False  # single lane, no merging allowed
            if (lane_left and not lane_left.distance_windows) and (lane_right and not lane_right.distance_windows):
                return False

            # TODO: maybe every car in every lane has a number associated
            # need to shift the correct x,y amount depending on which window/ how close
            # cars can only merge forward
            # determine which lane to add to
            left_distances = None
            right_distances = None
            if lane_left is not None and len(lane_left.distance_windows) != 0:
                left_distances = lane_left.distance_windows
                if len(left_distances) < 4:
                    return False
            if lane_right is not None and len(lane_right.distance_windows) != 0:
                right_distances = lane_right.distance_windows
                if len(right_distances) < 4:
                    return False

            largest_distance = 0
            largest_idx = None
            lane_to_merge = None

            # could have ONLY left lane, ONLY right lane, BOTH, or NONE
            # idx: signifies current car index in THAT lane, lanes[lane_number].indexOf(self)
            idx_of_car_in_lane = lanes[self.lane_number].lane_cars_list.index(self)

            # not letting first car merge
            if idx_of_car_in_lane == 0 or idx_of_car_in_lane + 1 >= len(lanes[self.lane_number].lane_cars_list) or \
                (left_distances is not None and idx_of_car_in_lane >= len(left_distances) - 1) or (right_distances is \
                    not None and idx_of_car_in_lane >= len(right_distances) - 1):
                self.state = CarState.CRUISING
                Car.merging_state = Merging.NO_MERGE
                return False

            print("left: ", lane_left, left_distances)
            print("right: ", lane_right, right_distances)
            print("idx: ", idx_of_car_in_lane)
            if lane_left and left_distances:
                possible_distances_l = {idx_of_car_in_lane: left_distances[idx_of_car_in_lane],
                                        (idx_of_car_in_lane - 1): left_distances[idx_of_car_in_lane - 1],
                                        (idx_of_car_in_lane + 1): left_distances[idx_of_car_in_lane + 1]}
                for key_l, val_l in possible_distances_l.items():
                    if val_l > largest_distance:
                        largest_distance = val_l
                        largest_idx = key_l
                        lane_to_merge = lane_left

            if lane_right and right_distances:
                possible_distances_r = {idx_of_car_in_lane: right_distances[idx_of_car_in_lane],
                                        (idx_of_car_in_lane - 1): right_distances[idx_of_car_in_lane - 1],
                                        (idx_of_car_in_lane + 1): right_distances[idx_of_car_in_lane + 1]}
                for key_r, val_r in possible_distances_r.items():
                    if val_r > largest_distance:
                        largest_distance = val_r
                        largest_idx = key_r
                        lane_to_merge = lane_right

            if largest_distance < 25:
                return False

            print("gonna merge")
            # 2. initiate merge
            self.state = CarState.MERGING
            Car.merging_state = Merging.MERGE_IN_PROGRESS
            currently_merging = True

            # 3. add THIS car in THIS lane to the OTHER lane; remove THIS car from THIS lane
            if lane_to_merge == lane_left:
                # lanes[self.lane_number].switch_lanes(lane_left, self, idx_of_car_in_lane, largest_idx)
                self.merging_direction = 0
            elif lane_to_merge == lane_right:
                # lanes[self.lane_number].switch_lanes(lane_right, self, idx_of_car_in_lane, largest_idx)
                self.merging_direction = 1
            print("returning True")
            print("merging", Car.merging_state)
            print("car", self.state)
            self.merging_lane = lane_to_merge
            self.car_index = idx_of_car_in_lane
            self.merging_index = largest_idx
            return True


    def continue_merge(self):
        global currently_merging, lane_y
        # 4. continuing merge
        if not currently_merging:
            # if Car.merging_state == Merging.MERGE_IN_PROGRESS and self.state == CarState.MERGING:
            # TODO: never returns to initiate_merge
            print("continuing merge")
            # Car.merging_state = Merging.MERGE_IN_PROGRESS
            print("car speed", self.car_speed)
            if self.merging_direction == 0:
                self.y -= 8  # (1.2 * self.car_speed)
            elif self.merging_direction == 1:
                self.y += 8  # (1.2 * self.car_speed)

            # TODO: merge count doesn't increase when switch_lanes runs
            lanes[self.lane_number].switch_lanes(self.merging_lane, self, self.car_index, self.merging_index)
            # 5. finishing merge
            Car.merge_count += 1
            if Car.merge_count == 4:
                print(f"reached the end with merge state: {self.merging_state} and car state: {self.state}")
                # self.state = CarState.CRUISING
            print("merge count", Car.merge_count)
            #if self.merge_count == 4:
            print("merge count finished")
            # self.state = CarState.CRUISING
            # Car.merging_state = Merging.NO_MERGE
            # currently_merging = False
            # self.merge_count = 0  # reset merge_count so next car can start merge
            # self.merging_direction = None  # reset merging_direction for next car
            # self.merging_lane = None
            # self.car_index = None
            # self.merging_index = None

    # TODO change how fast cars accelerate and brake depending on the state
    def brake(self, car_distance):
        # gradually slow down
        self.state = CarState.BRAKING
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
        self.state = CarState.ACCELERATING

    # TODO configure the reaction times to be dependent on the state of the car
    def react(self, sleep_time=0):
        # react to the car in front of you
        self.react_time = sleep_time

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.car_radius)


# TODO create a function that allows cars to change lanes

# Game loop
running = True
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)  # You can specify the font file and size

# Create lanes
lanes = []
for i in range(num_lanes):
    lane_cars = Lane()
    lanes.append(lane_cars)

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

counter = 0
game_set = False

# Create the slider
slider = Slider(900, 100, slider_width, slider_height, handle_width, handle_height, slider_color,
                slider_handle_color)
merge_lane = Ramp(merge_lane_x, merge_lane_y, "merge")
exit_lane = Ramp(exit_lane_x, exit_lane_y, "exit")

while running and counter < 100:

    screen.fill(green)

    plus_button = PlusButton(1250, 30)
    minus_button = MinusButton(1180, 30)
    set_button = Button(675, 500, "Go")

    # Draw the highway
    pygame.draw.rect(screen, gray, (lane_x, lane_y, lane_width, all_lanes_height))

    plus_button.is_hover()
    minus_button.is_hover()
    set_button.is_hover()
    merge_lane.is_hovered()
    exit_lane.is_hovered()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if set_button.handle_event(event):
            game_init()
            set_button.undraw()
            game_set = True
        slider.handle_event(event)
        plus_button.handle_event(event)
        minus_button.handle_event(event)
        merge_lane.handle_event(event)
        exit_lane.handle_event(event)

    plus_button.draw(screen)
    minus_button.draw(screen)
    slider.draw(screen)
    merge_lane.draw(screen)
    exit_lane.draw(screen)
    if not game_set:
        set_button.draw(screen)

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
    roads_text = font.render("No. of Roads: " + str(num_lanes), True, black)
    screen.blit(roads_text, (980, 45))
    ramp_width_text = font.render("Ramp Width: " + str(exit_ramp_width), True, black)
    screen.blit(ramp_width_text, (980, 10))

    print("spawn count: ", spawn_count)
    for lane in lanes:
        lane.display()
        
    # Spawn cars
    if game_set:
        spawn_cars()


    pygame.display.update()
    clock.tick(60)

# Quit the game
pygame.quit()
