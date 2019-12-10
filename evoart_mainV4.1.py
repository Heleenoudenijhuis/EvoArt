from threading import Thread
import math
import random
import time
import numpy as np
from pynput.mouse import Button, Controller
from pynput.keyboard import Key, Listener
import os
import pynput

mouse = Controller()
#---------------------------------------------------ERRORS--------------------------------------------------------#
#if keystrokes don't show any message while selecting parents. Check the on_click function. Different pythons
#take in different indexies for the keystrokes. So instead of key[1] you might need key[2]..
#-----------------------------------------------------------------------------------------------------------------#


# remove all objects before running this script.
# bpy.ops.object.select_all(action='SELECT')
# bpy.ops.object.delete(use_global=False, confirm=False)

# the class shave will generate an object which represents the shapes in blender.
# all the objects have the same attributes and functions.
# locations should change, and be split over 4 places in the blender xy 2D plane.
class Shape():
    def __init__(self, location_x,location_y,location_z,parameter,mesh_type,mesh_size,mesh_length,mesh_length_y,segments,number,number2,color_scheme,color_varaiation,color_h,color_s,color_v,color_a):  #location
        self.location_x = location_x
        self.location_y = location_y
        self.location_z = location_z
        #parameter control
        self.parameter = parameter
        self.mesh_type = mesh_type
        self.mesh_size = mesh_size
        self.mesh_length = mesh_length
        self.mesh_length_y = mesh_length_y
        self.segments = segments
        self.number = number
        self.number2 = number2
        #color control
        self.color_scheme = color_scheme
        self.color_variation = color_varaiation
        self.color_h = color_h
        self.color_s = color_s
        self.color_v = color_v
        self.color_a = color_a
        self.sigma = 1.0
        self.full_list = [self.location_x,self.location_y,self.location_z,self.parameter,self.mesh_type,self.mesh_size,self.mesh_length,self.mesh_length_y,self.segments,self.number,self.number2,self.color_scheme,self.color_variation,self.color_h,self.color_s,self.color_v,self.color_a]

    #this function takes all self.inputs, and changes them based on the draw from a normal gaussian distribution. the arguments are self. Sigma as std (step size), with the original data as mean.
    def mutation(self):
        # parameter control
        self.parameter = make_float(np.random.normal(self.parameter,(0.2*self.sigma)))
        self.mesh_type = make_float(np.random.normal(self.mesh_type,(0.5*self.sigma)))
        self.mesh_size = make_float(np.random.normal(self.mesh_size,(0.01*self.sigma)))
        self.mesh_length = make_float(np.random.normal(self.mesh_length,(0.5*self.sigma)))
        self.mesh_length_y = make_float(np.random.normal(self.mesh_length_y,self.sigma))
        self.segments = make_float(np.random.normal(self.segments,self.sigma))
        self.number = make_float(np.random.normal(self.number,self.sigma))
        self.number2 = make_float(np.random.normal(self.number2,self.sigma))
        # color control
        self.color_sceme = make_float(np.random.normal(self.color_scheme,(0.3*self.sigma)))
        self.color_variation = make_float(np.random.normal(self.color_variation,(0.01*self.sigma)))
        self.color_h = make_float(np.random.normal(self.color_h,(0.05*self.sigma)))
        self.color_s = make_float(np.random.normal(self.color_s,(0.1*self.sigma)))
        self.color_v = make_float(np.random.normal(self.color_v,(0.05*self.sigma)))
        self.color_a = make_float(np.random.normal(self.color_a,(0.01*self.sigma)))
        self.full_list = [self.location_x, self.location_y, self.location_z, self.parameter, self.mesh_type,
                          self.mesh_size, self.mesh_length, self.mesh_length_y, self.segments, self.number,
                          self.number2, self.color_scheme, self.color_variation, self.color_h, self.color_s,
                          self.color_v, self.color_a]

    #funtion for testing, to print all self information
    def printing(self):
        print(self, self.location_x, self.location_y, self.location_z, self.parameter, self.mesh_type,
                          self.mesh_size, self.mesh_length, self.mesh_length_y, self.segments, self.number,
                          self.number2, self.color_scheme, self.color_variation, self.color_h, self.color_s,
                          self.color_v, self.color_a)

        #this function will print all genes to a txt file seperated by "," so that they can be taken by blender as a list.
    def print_to_txt(self,file):
        self_object_list = [self.location_x, self.location_y, self.location_z, self.parameter, self.mesh_type,
                          self.mesh_size, self.mesh_length, self.mesh_length_y, self.segments, self.number,
                          self.number2, self.color_scheme, self.color_variation, self.color_h, self.color_s,
                          self.color_v, self.color_a]
        for object in self_object_list:
            # counter.main_parameter_check(object,number)
            file.write(str(object))
            file.write(",")
        file.write("\n")

    def main_parameter_check(self):
        self.parameter = self.parameter_check(counter.limit_list[0][0], counter.limit_list[0][1], self.parameter)
        self.mesh_type = self.other_limits_check(counter.limit_list[1][0], counter.limit_list[1][1], self.mesh_type)
        self.mesh_size = self.other_limits_check(counter.limit_list[2][0], counter.limit_list[2][1], self.mesh_size)
        self.mesh_length = self.other_limits_check(counter.limit_list[3][0], counter.limit_list[3][1],
                                                     self.mesh_length)
        self.mesh_length_y = self.other_limits_check(counter.limit_list[4][0], counter.limit_list[4][1],
                                                       self.mesh_length)
        self.segments = self.other_limits_check(counter.limit_list[5][0], counter.limit_list[5][1], self.segments)
        self.number = self.other_limits_check(counter.limit_list[6][0], counter.limit_list[6][1], self.number)
        self.number2 = self.other_limits_check(counter.limit_list[7][0], counter.limit_list[7][1], self.number2)
        self.color_scheme = self.other_limits_check(counter.limit_list[8][0], counter.limit_list[8][1],
                                                      self.color_scheme)
        self.color_variation = self.other_limits_check(counter.limit_list[9][0], counter.limit_list[9][1],self.color_variation)
        self.color_h = self.other_limits_check(counter.limit_list[10][0], counter.limit_list[10][1], self.color_h)
        self.color_s = self.other_limits_check(counter.limit_list[11][0], counter.limit_list[11][1], self.color_s)
        self.color_v = self.other_limits_check(counter.limit_list[12][0], counter.limit_list[12][1], self.color_v)
        self.color_a = self.other_limits_check(counter.limit_list[13][0], counter.limit_list[13][1], self.color_a)

    def parameter_check(self, minimum, maximum, value):
        while value < minimum or value > maximum:
            if value < minimum:
                value = maximum - abs(value)
            elif value > maximum:
                value = minimum + (value - maximum)
        return value

    def other_limits_check(self, minimum,maximum, value):
        while value < minimum or value > maximum:
            if value < minimum:
                value = minimum + abs(value)
            elif value > maximum:
                value = maximum - (value - maximum)
        return value

class Counter():
    def __init__(self):
        self.select_one = 0 #boolean if 1 is selected
        self.select_two = 0 #boolean if 2 is selected
        self.select_three = 0 #boolean if 3 is selected
        self.select_four = 0 #boolean if 4 is selected
        self.selected_list = [self.select_one,self.select_two,self.select_three,self.select_four]
        self.total_selected = 0 #total amount of selected objects
        self.total_generations = 0 #num of generations since initiation from music group
        self.previous_generation = [0,0,0,0]
        self.autopilot = 0
        self.time = time.time()
        self.backspace = 0

        #gene parameter settings below as lists, where index 0 indicates minimum, 1 indicates maximum
        self.parameter_limits = [0.0,8.0]
        self.mesh_type_limits = [0.0,7.0]
        self.mesh_size_limits = [1.0,2.0]
        self.mesh_length_limits = [1.0,10.0]
        self.mesh_length_y_limits = [1.0,10.0]
        self.segments_limits = [1.0,10.0]
        self.number_limits = [1.0,10.0]
        self.number2_limits = [1.0,10.0]
        self.color_scheme_limits = [0.0,5.0]
        self.color_variation_limits = [0.00,0.05]
        self.color_h_limits = [0.0,1.0]
        self.color_s_limits = [0.5,1.0]
        self.color_v_limits = [0.5,1.0]
        self.color_a_limits = [0.,1.0]
        self.limit_list = [self.parameter_limits, self.mesh_type_limits, self.mesh_size_limits, self.mesh_length_limits,
                           self.mesh_length_y_limits, self.segments_limits, self.number_limits, self.number2_limits,
                           self.color_scheme_limits, self.color_variation_limits, self.color_h_limits,
                           self.color_s_limits, self.color_v_limits, self.color_a_limits]

#main selected is the selection tool for keystrokes and keeps track of what keystroke is selected and what function to  go to.
#one,two,three,four _selected are simple if functions which keep track of which object is selected at any time, by simply changing self....
#to 1 or to 0 as booleans.
    def main_selected(self,input):
        if input == "1":
            self.one_selected()
        elif input == "2":
            self.two_selected()
        elif input == "3":
            self.three_selected()
        elif input == "4":
            self.four_selected()
        else:
            pass

    def one_selected(self):
        if self.select_one == 1:
            self.select_one = 0
            self.total_selected = self.total_selected - 1
            self.selected_list = [self.select_one, self.select_two, self.select_three, self.select_four]
            print("one deselected")
        elif self.select_one == 0:
            self.select_one = 1
            self.total_selected = self.total_selected + 1
            self.selected_list = [self.select_one, self.select_two, self.select_three, self.select_four]
            print("one selected")
        print("total selected = " + str(self.total_selected))


    def two_selected(self):
        if self.select_two == 1:
            self.select_two = 0
            self.total_selected = self.total_selected - 1
            self.selected_list = [self.select_one, self.select_two, self.select_three, self.select_four]
            print("two deselected")
        elif self.select_two == 0:
            self.select_two = 1
            self.total_selected = self.total_selected + 1
            self.selected_list = [self.select_one, self.select_two, self.select_three, self.select_four]
            print("two selected")
        print("total selected = " + str(self.total_selected))

    def three_selected(self):
        if self.select_three == 1:
            self.select_three = 0
            self.total_selected = self.total_selected - 1
            self.selected_list = [self.select_one, self.select_two, self.select_three, self.select_four]
            print("three deselected")
        elif self.select_three == 0:
            self.select_three = 1
            self.total_selected = self.total_selected + 1
            self.selected_list = [self.select_one, self.select_two, self.select_three, self.select_four]
            print("three selected")
        print("total selected = " + str(self.total_selected))

    def four_selected(self):
        if self.select_four == 1:
            self.select_four = 0
            self.total_selected = self.total_selected - 1
            self.selected_list = [self.select_one, self.select_two, self.select_three, self.select_four]
            print("four selected")
        elif self.select_four == 0:
            self.select_four = 1
            self.total_selected = self.total_selected + 1
            self.selected_list = [self.select_one, self.select_two, self.select_three, self.select_four]
            print("four selected")
        print("total selected = " + str(self.total_selected))

#this function resets all selected values back to 0, after the parents are selected by pressing enter.
    def reset_timer(self):
        self.autopilot = 0
        self.time = time.time()

    def reset(self):
        self.total_selected = 0
        self.select_one = 0  # boolean if 1 is selected
        self.select_two = 0  # boolean if 2 is selected
        self.select_three = 0  # boolean if 3 is selected
        self.select_four = 0  # boolean if 4 is selected
        self.autopilot = 0 #boolean if there has been interaction since last press

# this list has initial locations for the 4 objects, one top-left, top-right, bottom-left, bottom-right.
location_list = [[-15, 15, 0], [15, 15, 0], [-15, -15, 0], [15, -15, 0]]

# here we initiate our 4 object that will be made in space
# the arguments given should come from the music group as csv and be read into "shave" via function.
one = Shape(-15,15,0,        0.8,1.0,7,10,11,61,13,3,0.03,5,0.2,2.3,0.11,0.5)
two = Shape(15,15,0,        0.8,2.0,7,10,11,61,13,3,0.03,5,0.2,2.3,0.11,0.5)
three = Shape(-15,-15,0,    0.8,3.0,7,10,11,61,13,3,0.03,5,0.2,2.3,0.11,0.5)
four = Shape(15,-15,0,      0.8,4.0,7,10,11,61,13,3,0.03,5,0.2,2.3,0.11,0.5)

#counter will keep track of all processes while the program is running.
counter = Counter()

#this list is used to cycle over all objects in a forloop.
object_list = [one, two, three, four]

def main_print(object_list):
    with open("objectinfo.txt", "w") as file:
        for shape in object_list:
            shape.printing()
            shape.print_to_txt(file)

main_print(object_list)

mouse.position = (1551, 243)
mouse.press(Button.left)
mouse.release(Button.left)
#generate initiaton function here directly taken from musicgroup

#this function will create new shape objects and transferes the object list of generation n  to these shapes.
#so the return function executed at generation n+1 can call back on these shapes. This has to be done because objects
#are loaded in the same bits, so changing them to old would overrite them as soon as they get changed by another function.
def previous_shapes(object_list):
    old_one = Shape(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
    imitate(old_one,object_list[0])
    old_two = Shape(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
    imitate(old_two,object_list[1])
    old_three = Shape(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
    imitate(old_three, object_list[2])
    old_four = Shape(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
    imitate(old_four, object_list[3])
    prev_shapes = [old_one,old_two,old_three,old_four]
    return prev_shapes

def backspace_function(object_list):
    counter.reset()
    main_print(object_list)

def make_float(info):
    return float(info)

#this function will select the objects stored in the counter.selected_list. It will find the objects that are selected as parents and places them in the
# function "crossover_opperator" as arguments.
def get_selected(object_list):
    prev_shapes = previous_shapes(object_list)
    object_selection_list = []
    for number in range(0,4):
        if counter.selected_list[number] != 0: #go over counter_selected_list to find which parents were selected.
            object_selection_list.append(object_list[number])
    print("Parents chose, making child!")
    crossover_opperator(object_selection_list[0],object_selection_list[1])
    return prev_shapes

def crossover_function(child_object,parent_one,parent_two):
    random_change = random.randint(1,101)
    random_parent = random.randint(1,2)
    if random_change < 90 or random_change == 90:
        if random_parent == 1:
            child_object.parameter = float(parent_one.parameter)
        elif random_parent == 2:
            child_object.parameter = float(parent_two.parameter)
    elif random_change > 90:
        child_object.parameter = random.uniform(0,10.1)
    else:
        print("something wrong in crossover opperator2")

    random_change = random.randint(1, 101)
    random_parent = random.randint(1, 2)
    if random_change < 90 or random_change == 90:
        if random_parent == 1:
            child_object.mesh_type = float(parent_one.mesh_type)
        elif random_parent == 2:
            child_object.mesh_type = float(parent_two.mesh_type)
    elif random_change > 90:
        child_object.mesh_type = random.uniform(0, 10.1)
    else:
        print("something wrong in crossover opperator2")

    random_change = random.randint(1, 101)
    random_parent = random.randint(1, 2)
    if random_change < 90 or random_change == 90:
        if random_parent == 1:
            child_object.mesh_size = float(parent_one.mesh_size)
        elif random_parent == 2:
            child_object.mesh_size = float(parent_two.mesh_size)
        else:
            print("something wrong in crossover opperator1")
    elif random_change > 90:
        child_object.mesh_size = random.uniform(0, 10.1)
    else:
        print("something wrong in crossover opperator2")

    random_change = random.randint(1, 101)
    random_parent = random.randint(1, 2)
    if random_change < 90 or random_change == 90:
        if random_parent == 1:
            child_object.mesh_length = float(parent_one.mesh_length)
        elif random_parent == 2:
            child_object.mesh_length = float(parent_two.mesh_length)
        else:
            print("something wrong in crossover opperator1")
    elif random_change > 90:
        child_object.mesh_length = random.uniform(0, 10.1)
    else:
        print("something wrong in crossover opperator2")

    random_change = random.randint(1, 101)
    random_parent = random.randint(1, 2)
    if random_change < 90 or random_change == 90:
        if random_parent == 1:
            child_object.mesh_length_y = float(parent_one.mesh_length_y)
        elif random_parent == 2:
            child_object.mesh_length_y = float(parent_two.mesh_length_y)
        else:
            print("something wrong in crossover opperator1")
    elif random_change > 90:
        child_object.mesh_length_y = random.uniform(0, 10.1)
    else:
        print("something wrong in crossover opperator2")

    random_change = random.randint(1, 101)
    random_parent = random.randint(1, 2)
    if random_change < 90 or random_change == 90:
        if random_parent == 1:
            child_object.segments = float(parent_one.segments)
        elif random_parent == 2:
            child_object.segments = float(parent_two.segments)
        else:
            print("something wrong in crossover opperator1")
    elif random_change > 90:
        child_object.segments = random.uniform(0, 10.1)
    else:
        print("something wrong in crossover opperator2")

    random_change = random.randint(1, 101)
    random_parent = random.randint(1, 2)
    if random_change < 90 or random_change == 90:
        if random_parent == 1:
            child_object.number = float(parent_one.number)
        elif random_parent == 2:
            child_object.number = float(parent_two.number)
        else:
            print("something wrong in crossover opperator1")
    elif random_change > 90:
        child_object.number = random.uniform(0, 10.1)
    else:
        print("something wrong in crossover opperator2")

    random_change = random.randint(1, 101)
    random_parent = random.randint(1, 2)
    if random_change < 90 or random_change == 90:
        if random_parent == 1:
            child_object.number2 = float(parent_one.number2)
        elif random_parent == 2:
            child_object.number2 = float(parent_two.number2)
        else:
            print("something wrong in crossover opperator1")
    elif random_change > 90:
        child_object.number2 = random.uniform(0, 10.1)
    else:
        print("something wrong in crossover opperator2")

    random_change = random.randint(1, 101)
    random_parent = random.randint(1, 2)
    if random_change < 90 or random_change == 90:
        if random_parent == 1:
            child_object.color_scheme = float(parent_one.color_scheme)
        elif random_parent == 2:
            child_object.color_scheme = float(parent_two.color_scheme)
        else:
            print("something wrong in crossover opperator1")
    elif random_change > 90:
        child_object.color_scheme = random.uniform(0, 10.1)
    else:
        print("something wrong in crossover opperator2")

    random_change = random.randint(1, 101)
    random_parent = random.randint(1, 2)
    if random_change < 90 or random_change == 90:
        if random_parent == 1:
            child_object.color_variation = float(parent_one.color_variation)
        elif random_parent == 2:
            child_object.color_variation = float(parent_two.color_variation)
        else:
            print("something wrong in crossover opperator1")
    elif random_change > 90:
        child_object.color_variation = random.uniform(0, 10.1)
    else:
        print("something wrong in crossover opperator2")

    random_change = random.randint(1, 101)
    random_parent = random.randint(1, 2)
    if random_change < 90 or random_change == 90:
        if random_parent == 1:
            child_object.color_h = float(parent_one.color_h)
        elif random_parent == 2:
            child_object.color_h = float(parent_two.color_h)
        else:
            print("something wrong in crossover opperator1")
    elif random_change > 90:
        child_object.color_h = random.uniform(0, 10.1)
    else:
        print("something wrong in crossover opperator2")

    random_change = random.randint(1, 101)
    random_parent = random.randint(1, 2)
    if random_change < 90 or random_change == 90:
        if random_parent == 1:
            child_object.color_s = float(parent_one.color_s)
        elif random_parent == 2:
            child_object.color_s = float(parent_two.color_s)
        else:
            print("something wrong in crossover opperator1")
    elif random_change > 90:
        child_object.color_s = random.uniform(0, 10.1)
    else:
        print("something wrong in crossover opperator2")

    random_change = random.randint(1, 101)
    random_parent = random.randint(1, 2)
    if random_change < 90 or random_change == 90:
        if random_parent == 1:
            child_object.color_v = float(parent_one.color_v)
        elif random_parent == 2:
            child_object.color_v = float(parent_two.color_v)
        else:
            print("something wrong in crossover opperator1")
    elif random_change > 90:
        child_object.color_v = random.uniform(0, 10.1)
    else:
        print("something wrong in crossover opperator2")

    random_change = random.randint(1, 101)
    random_parent = random.randint(1, 2)
    if random_change < 90 or random_change == 90:
        if random_parent == 1:
            child_object.color_a = float(parent_one.color_a)
        elif random_parent == 2:
            child_object.color_a = float(parent_two.color_a)
        else:
            print("something wrong in crossover opperator1")
    elif random_change > 90:
        child_object.color_a = random.uniform(0, 10.1)
    else:
        print("something wrong in crossover opperator2")
    return child_object

def uniform_crossover_function(child_object):
    child_object.location_x = 0
    child_object.location_y = 0
    child_object.location_z = 0
    # parameter control
    child_object.parameter = random.uniform(0.00,8.00)
    child_object.mesh_type = random.uniform(0.00,7.00)
    child_object.mesh_size = random.uniform(1.00,2.00)
    child_object.mesh_length = random.uniform(1.00,10.00)
    child_object.mesh_length_y = random.uniform(1.00,10.00)
    child_object.segments = random.uniform(1.00,10.00)
    child_object.number = random.uniform(1.00,10.00)
    child_object.number2 = random.uniform(1.00,10.00)
    # color control
    child_object.color_scheme = random.uniform(0.00,5.00)
    child_object.color_variation = random.uniform(0.00,0.05)
    child_object.color_h = random.uniform(0.00,1.00)
    child_object.color_s = random.uniform(0.50,1.00)
    child_object.color_v = random.uniform(0.00,1.00)
    child_object.color_a = random.uniform(0.90,1.00)
    child_object.sigma = 3.0
    child_object.full_list = [child_object.location_x, child_object.location_y, child_object.location_z, child_object.parameter, child_object.mesh_type, child_object.mesh_size,
                              child_object.mesh_length, child_object.mesh_length_y, child_object.segments, child_object.number, child_object.number2, child_object.color_scheme,
                              child_object.color_variation, child_object.color_h, child_object.color_s, child_object.color_v, child_object.color_v]
    return child_object

#the function crossover_opperator will take two parents as arguments. and create a Child_object, which is an average recombination of both parents.
#the childobject will be used as argument for the function replace, which will dictate the change from old objects to new objects.

def crossover_opperator(parent_one,parent_two):
    test_parent = Shape(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
    test_parent_two = Shape(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    imitate(test_parent,parent_one)
    imitate(test_parent_two,parent_two)
    #child one
    child_object = Shape(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
    child_object = crossover_function(child_object,test_parent,test_parent_two)
    child_object.full_list = [child_object.location_x,child_object.location_y,child_object.location_z,child_object.parameter,child_object.mesh_type,child_object.mesh_size,child_object.mesh_length,child_object.mesh_length_y,child_object.segments,child_object.number,child_object.number2,child_object.color_scheme,child_object.color_variation,child_object.color_h,child_object.color_s,child_object.color_v,child_object.color_a]
    imitate(object_list[0], child_object)
    one.location_x = -15
    one.location_y = 15
    one.location_z = 0
    one.main_parameter_check()

#child two
    child_object = Shape(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    child_object = crossover_function(child_object,test_parent,test_parent_two)
    child_object.full_list = [child_object.location_x, child_object.location_y, child_object.location_z,
                              child_object.parameter, child_object.mesh_type, child_object.mesh_size,
                              child_object.mesh_length, child_object.mesh_length_y, child_object.segments,
                              child_object.number, child_object.number2, child_object.color_scheme,
                              child_object.color_variation, child_object.color_h, child_object.color_s,
                              child_object.color_v, child_object.color_a]
    imitate(object_list[1], child_object)
    two.location_x = 15
    two.location_y = 15
    two.location_z = 0
    # object_list[1].mutation()
    two.main_parameter_check()

#child three
    child_object = Shape(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    child_object= crossover_function(child_object,test_parent,test_parent_two)
    child_object.full_list = [child_object.location_x, child_object.location_y, child_object.location_z,
                              child_object.parameter, child_object.mesh_type, child_object.mesh_size,
                              child_object.mesh_length, child_object.mesh_length_y, child_object.segments,
                              child_object.number, child_object.number2, child_object.color_scheme,
                              child_object.color_variation, child_object.color_h, child_object.color_s,
                              child_object.color_v, child_object.color_a]
    imitate(object_list[2], child_object)
    three.location_x = -15
    three.location_y = -15
    three.location_z = 0
    # object_list[2].mutation()
    three.main_parameter_check()

#child four
    child_object = Shape(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    child_object = uniform_crossover_function(child_object)
    child_object.full_list = [child_object.location_x, child_object.location_y, child_object.location_z,
                              child_object.parameter, child_object.mesh_type, child_object.mesh_size,
                              child_object.mesh_length, child_object.mesh_length_y, child_object.segments,
                              child_object.number, child_object.number2, child_object.color_scheme,
                              child_object.color_variation, child_object.color_h, child_object.color_s,
                              child_object.color_v, child_object.color_a]
    imitate(object_list[3], child_object)
    # object_list[3].sigma = 3  # mutation stepsize increase for last object mutation
    four.location_x = 15
    four.location_y = -15
    four.location_z = 0
    # object_list[3].mutation()
    four.main_parameter_check()

#the function replace will go over every object, and replace the population. This is done with the imitate function, so that all object values are replaced
#by the child values, mutated accordingly, and extra values set to the right ones.
#the reason for this is because, when using one = child_object... the computer saves all information in the same place and all objects become one.
#this way changes the objects values directly in the general object_list, while all objects remain their original name (one,two,three,four).


#imitate takes two arguments, the object one,two,three,four, and the child_object and set's all values from objects to child object.
def imitate(object_one,object_two):
    object_one.location_x = object_two.location_x
    object_one.location_y = object_two.location_y
    object_one.location_z = object_two.location_z
    # parameter control
    object_one.parameter = object_two.parameter
    object_one.mesh_type = object_two.mesh_type
    object_one.mesh_size = object_two.mesh_size
    object_one.mesh_length = object_two.mesh_length
    object_one.mesh_length_y = object_two.mesh_length_y
    object_one.segments = object_two.segments
    object_one.number = object_two.number
    object_one.number2 = object_two.number2
    object_one.color_scheme = object_two.color_scheme
    object_one.color_variation = object_two.color_variation
    object_one.color_h = object_two.color_h
    object_one.color_s = object_two.color_s
    object_one.color_v = object_two.color_v
    object_one.color_a = object_two.color_a
    object_one.full_list = object_two.full_list

    # This is the function that will be executed when a button is pressed in the while loop.
    # see this function as the selection function.

def press_in_blender(x,y):
    mouse.position = (x, y)
    mouse.press(Button.left)
    mouse.release(Button.left)

def on_press(key):
    # add key for selection any of the four shapes in blender.
    input = '{0}'.format(key)[1]  # translate the overal "key" to one single keystroke.
    print(input)
    counter.reset_timer()

    # every keyinput will be put into this counter, if the key is 1,2,3 or 4, the counter will keep track of a selection which objects are selected
    # and what the total amount of selected objects is.
    counter.main_selected(input)

    # stop the listener
    if key == Key.enter and counter.total_selected == 2:
        counter.total_generations += 1  # interesting to keep track of total amound of generations after initiation.
        return False
    elif key == Key.backspace:
        counter.backspace = 1
        print("shapes reset to previous iteration")
        return False
    elif key == Key.enter and counter.total_selected != 2:
        print("not a total of 2 parents are selected, please select the right amount of parents")

#this line will run till enter is pressed, and only when 2 parents are selected.
def listener_function():
    print('function_one running')
    while True:
        with Listener(on_press=on_press) as listener:
            listener.join()
        if counter.backspace == 1:
            backspace_function(old_object_list)
            counter.backspace = 0
            counter.reset()  # reset the counter after new objects are made
            press_in_blender(1551, 243)  # press the run script button inside blender to automaticly generate shapes.
        elif counter.backspace != 1:
            old_object_list = get_selected(object_list)
            counter.reset()  # reset the counter after new objects are made
            press_in_blender(1551, 243)  # press the run script button inside blender to automaticly generate shapes.
            main_print(object_list)
        else:
            print("error in listener_function: no txt file update")

def timer(object_list):
    print("function two running")
    while True:
        while not (time.time() - counter.time >= 59):
            print("no two minutes have passes, waiting for 10 seconds")
            time.sleep(10)
        #do nothing
        print("autopilot on")
        counter.autopilot = 1
        while counter.autopilot == 1:
            random_interger_one = 0
            random_interger_two = 0
            while random_interger_one == random_interger_two:
                random_interger_one = str(np.random.randint(1,5,dtype="int"))
                random_interger_two = str(np.random.randint(1,5,dtype="int"))
            counter.main_selected(random_interger_one)
            counter.main_selected(random_interget_two)

    # here the crossover function will happen, which makes "one" the original crossover child from the parents and "two","three","four", mutation of the child "one".
    # counter.get_selected will find out which objects are selected and makes a list with objects, which will be used as arguments for the crossover function.
    # which takes two argument objects, and will preform crossover from the objects.
        old_object_list = get_selected(object_list)
        counter.reset()# reset the counter after new objects are made
        press_in_blender(1551,243)#press the run script button inside blender to automaticly generate shapes.
        main_print(object_list)
        print("made by autopilot")
        time.sleep(30)


#The program are two while loops who loop paralel too each other
thread_one = Thread(target=listener_function())
# thread_two = Thread(target=timer(object_list))
thread_one.start()
# thread_two.join()