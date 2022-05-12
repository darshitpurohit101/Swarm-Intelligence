#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 14:20:27 2022

@author: darshit
"""
import numpy as np
import random
from math import *
import matplotlib.pyplot as plt
from datetime import datetime
import tqdm 
class hearding():
    def __init__(self,gs,no_wolf,numeric_mat,wolf_locations,prey_location,k):
        self.gs = gs
        self.no_wolf = no_wolf
        self.numeric_mat = numeric_mat
        self.predator_locations = predator_locations
        self.prey_location = prey_location
        self.replusive_rate = k
        self.state= True
        
    def distance(self,possible_moves,prey_surround,predators):
        cell_values = []
        for mv in possible_moves:
            predator_prey_distances = []
            for sur in prey_surround:#[N,E,S,W]
                d = self.euclidean_distance(mv, sur)
                predator_prey_distances.append(d)
            predator_predator_distance = []
            for predator in predators:
                d = self.euclidean_distance(mv,predator)
                predator_predator_distance.append(d)
            distance = min(predator_prey_distances) - self.replusive_rate*(sum(predator_predator_distance))
            cell_values.append(distance)
        return cell_values
        
    def euclidean_distance(self,src,dst):
        distance = [abs(val1-val2)**2 for val1,val2 in zip(src, dst)]
        euclidean_distance = sum(distance)**0.5
        return euclidean_distance
    
    def neighbours(self,current_loc):
        temp_loc = current_loc
        temp_moves = [[temp_loc[0]-1,temp_loc[1]], #0
                      [temp_loc[0]-1,temp_loc[1]+1], #1
                      [temp_loc[0],temp_loc[1]+1], #2
                      [temp_loc[0]+1,temp_loc[1]+1], #3
                      [temp_loc[0]+1,temp_loc[1]], #4
                      [temp_loc[0]+1,temp_loc[1]-1], #5
                      [temp_loc[0],temp_loc[1]-1], #6
                      [temp_loc[0]-1,temp_loc[1]-1]] #7 
        
        return temp_moves
    
    def prey_surround(self,prey_loc, predator_locations):
        temp = [[prey_loc[0]-1,prey_loc[1]], #0
                      [prey_loc[0]-1,prey_loc[1]+1], #1
                      [prey_loc[0],prey_loc[1]+1], #2
                      [prey_loc[0]+1,prey_loc[1]+1], #3
                      [prey_loc[0]+1,prey_loc[1]], #4
                      [prey_loc[0]+1,prey_loc[1]-1], #5
                      [prey_loc[0],prey_loc[1]-1], #6
                      [prey_loc[0]-1,prey_loc[1]-1]] #7
        surrounds = []
        for i in temp:#check if the cell is in the mat
            if 0<=i[0]<self.gs and 0<=i[1]<self.gs:
                if i not in predator_locations:
                    surrounds.append(i)
        return surrounds, temp
    
    def visual(self, prey, predators):
        x,y = [],[]
        for i in predators:
            x.append(i[0])
            y.append(i[1])
        fig = plt.figure()  
        axes = plt.gca()
        axes.set_xlim(-2, self.gs+2)
        axes.set_ylim(-2, self.gs+2)
        axes.set_facecolor("green")
        
        axes.set_xticks( np.linspace(*axes.get_xlim(), num=2) ) 
        axes.set_yticks( np.linspace(*axes.get_ylim(), num=2) ) 
        axes.set_aspect( axes.get_xlim()[1]/axes.get_ylim()[1] * 1/1  ) 
        
        pey_loc = axes.plot(prey[0], prey[1], 'w.') #blue for prey
        predators_loc = axes.plot(x,y, 'k.') #red for predator
        plt.grid()
        plt.pause(0.15)
        plt.show()
        plt.close()

gs = 40
no_wolf = 8
numeric_mat = np.arange(gs*gs).reshape(gs,gs)
predator_locations = [random.sample(range(0,gs),2) for i in range(no_wolf)]
prey_location = random.sample(range(0,gs), 2)
min_dist_to_maintain = 5
linear_move = 0 #initialising, index of for next move
repulsive_rate = 0.08
linear_move = 0 #initialising, index of for next move
''' 0:Random
    1:Maximize
    2:Maintain minimum distance
    3:Staic'''
method = [0,1,2,3]
option = 3
flag = True

game = hearding(gs,no_wolf,numeric_mat,predator_locations,prey_location,repulsive_rate)
game.visual(prey_location, predator_locations)

while flag==True:
    game.visual(prey_location, predator_locations)
    if method[option] != 3:
        prey_temp_moves = game.neighbours(prey_location)
        prey_moves = []
        for i in prey_temp_moves:
            if 0<=i[0]<gs and 0<=i[1]<gs:
                if i not in predator_locations:
                    prey_moves.append(i)
        if len(prey_moves) == 0: #If prey can not move, then terminate
            flag = False
            break
        if method[option]==0: #Random movement
            prey_moves_index = [i for i in range(len(prey_moves))]
            prey_next_move = random.sample(prey_moves_index,1)
            prey_location = prey_moves[prey_next_move[0]]
        elif method[option]==1: #Maximize distance from the predator
            prey_cell_values = []
            nearest_prey_location = []
            for j in prey_moves:
                temp_dist = []
                for k in predator_locations:
                    d = game.euclidean_distance(j,k)
                    temp_dist.append(d)
                prey_cell_values.append(min(temp_dist))
            prey_next_move_index = prey_cell_values.index(max(prey_cell_values))
            prey_location = prey_moves[prey_next_move_index]
        elif method[option]==2: #keep minimum dist from predtor or else move linearly
            nearest_predators = []
            farthest_predators = []
            prey_min_cell_values = []
            prey_max_cell_values = []
            for j in prey_moves:
                temp_dist = []
                for k in predator_locations:
                    d = game.euclidean_distance(j,k)
                    temp_dist.append(d)
                nearest_predator = predator_locations[temp_dist.index(min(temp_dist))]
                farthest_predator = predator_locations[temp_dist.index(max(temp_dist))]
                if nearest_predator not in nearest_predators:
                    nearest_predators.append(nearest_predator)
                prey_min_cell_values.append(min(temp_dist))
                prey_max_cell_values.append(max(temp_dist))
            if len(prey_min_cell_values)!=0: 
                if min(prey_min_cell_values) <= min_dist_to_maintain:
                    prey_next_move_index = prey_min_cell_values.index(max(prey_min_cell_values))
                    linear_move = prey_next_move_index
                    prey_location = prey_moves[prey_next_move_index]
                else:
                    if linear_move > len(prey_moves)-1:
                        prey_location = prey_min_cell_values.index(max(prey_min_cell_values))
                        linear_move = prey_next_move_index
                    else:
                        prey_location = prey_moves[linear_move]
            else:
                if linear_move > len(prey_moves)-1:
                        prey_location = prey_min_cell_values.index(max(prey_min_cell_values))
                        linear_move = prey_next_move_index
                else:
                        prey_location = prey_moves[linear_move]
    
    '''iterating throung all the predators for the next moves'''
    for loc in range(len(predator_locations)):
        '''check if predator can move, if it is allready surrounding the prey'''
        surrounds, temp_surrounds = game.prey_surround(prey_location, predator_locations)
        if len(surrounds)==0:
            flag=False
            game.visual(prey_location, predator_locations)
            flag = False
            break
        '''terminate if prey is surrounded from 4 direction'''
        if predator_locations[loc] in temp_surrounds:
            continue
        temp_moves = game.neighbours(predator_locations[loc])
        moves = []
        for i in temp_moves:
            if 0<=i[0]<gs and 0<=i[1]<gs:
                if i != prey_location:
                    if i not in predator_locations:
                        moves.append(i)
        if len(moves)!=0:
            moves_index = [i for i in range(len(moves))]
            cell_values = game.distance(moves, surrounds, predator_locations)
            next_move = cell_values.index(min(cell_values))
            predator_locations[loc] = moves[next_move]
        