import matplotlib.pyplot as plt
import random
from collections import defaultdict
import numpy as np
from datetime import datetime
import csv

import seaborn as sn


class play():
    def __init__(self,grid_size,no_of_food_sources, no_of_ants, difusion_rate, evaporation_rate):
        self.terminal = False
        self.difusion_rate = difusion_rate
        self.evaporation_rate = evaporation_rate
        self.no_of_food_sources = no_of_food_sources
        self.no_of_ants = no_of_ants
        self.grid_size = grid_size
        self.board = np.arange(1,self.grid_size*self.grid_size+1).reshape(self.grid_size,self.grid_size)
        # self.locations = np.random.choice(self.board.ravel(),no_of_food_sources+1, replace=False)
        self.locations = [1421,123,434] # for comparing
        
    def initial_state(self):
        self.loc = self.locations.copy()
        x,y = np.where(self.board == self.locations[0])
        self.locations = np.delete(self.locations,[0]) #removing the index 0 (food location)
        sx, sy = [], []
        for i in self.locations:
            tempx, tempy = np.where(self.board == i)
            sx.append(tempx)
            sy.append(tempy)
        self.mapper = defaultdict(lambda: {'type':{1:0, 2:0}}) 
        self.ants = defaultdict(lambda: [0,self.loc[0]]) 
        
        return x,y,sx,sy,self.grid_size, self.board, self.ants, self.terminal, self.loc, self.mapper

        
    def move(self, ph_type, ant_loc):
        current_loc = ant_loc
        seeking_ph = ph_type
        
        back = current_loc + self.grid_size
        front = current_loc - self.grid_size
        right = current_loc + 1
        left = current_loc - 1
        right_top_diag = current_loc - (self.grid_size-1)
        left_top_diag = current_loc - (self.grid_size+1)
        right_bottom_diag = current_loc + (self.grid_size+1)
        left_bottom_diag = current_loc + (self.grid_size-1) 
        
        # temp_moves = [back, front, right, left, right_top_diag, left_top_diag, right_bottom_diag, left_bottom_diag]
        temp_moves = [front, right_top_diag, right, right_bottom_diag, back, left_bottom_diag, left, left_top_diag]
        legal_moves = [i for i in temp_moves if 0 < i <= self.grid_size*self.grid_size]        
        
        '''probabilistic approach '''
        ep = 1
        ph_values = [self.mapper[move]['type'][seeking_ph] + ep for move in legal_moves]
        probs = [val/sum(ph_values) for val in ph_values]
        next_move = np.random.choice(legal_moves , p=probs)
        
        if seeking_ph == 1:
            dispose_ph = 2
        else:
            dispose_ph = 1
            
        self.difusion(self.difusion_rate, current_loc, dispose_ph)
        self.evaporation(self.evaporation_rate)
        
        return next_move
    
    def difusion(self, rate, current_loc, seeking_ph):
        back = current_loc + self.grid_size
        front = current_loc - self.grid_size
        right = current_loc + 1
        left = current_loc - 1
        right_top_diag = current_loc - (self.grid_size-1)
        left_top_diag = current_loc - (self.grid_size+1)
        right_bottom_diag = current_loc + (self.grid_size+1)
        left_bottom_diag = current_loc + (self.grid_size-1) 
        
        fact = rate/100
        temp_moves = [back, front, right, left, right_top_diag, left_top_diag, right_bottom_diag, left_bottom_diag]
        sq_1_operations = temp_moves
        sq_2_operations = [temp_moves[0]+self.grid_size, temp_moves[1]-self.grid_size, temp_moves[2]+1, temp_moves[3]-1,
                           temp_moves[4]-(self.grid_size-1), temp_moves[5]+(self.grid_size-1), temp_moves[6]+(self.grid_size+1),
                           temp_moves[7]+(self.grid_size-1), temp_moves[4]-((self.grid_size-1)-self.grid_size), temp_moves[4]-((self.grid_size-2)), 
                           temp_moves[5]+(self.grid_size+2), temp_moves[5]+((self.grid_size-1)-self.grid_size), temp_moves[6]+(self.grid_size+2),
                           temp_moves[6]+((self.grid_size+1)+self.grid_size), temp_moves[6]+(self.grid_size+1), temp_moves[7]+(self.grid_size-2),
                           temp_moves[7]+((self.grid_size-1)+self.grid_size)]

        self.mapper[current_loc]['type'][seeking_ph] = 60
        for i in sq_1_operations:
            self.mapper[i]['type'][seeking_ph] = fact*60
        for j in sq_2_operations:
            self.mapper[j]['type'][seeking_ph] = fact*(fact*60)
                   
    def evaporation(self, rate):
        fact = (100-rate)/100
        
        for k in self.mapper.keys():
            for tp, ph in self.mapper[k]['type'].items():
                if fact * ph == 0.0:
                    cal = 0
                else:
                    cal = fact * ph
                self.mapper[k]['type'][tp] = cal
                    
    def ph_visual(self):
        phx, phy = [], []
        color_1, color_2 = [], []
        
        for k in self.mapper.keys():
            tempx, tempy = np.where(self.board == k)
            if tempx.size != 0 or tempy.size != 0:
                
                phx.append(int(tempx))
                phy.append(int(tempy))
                for tp, ph in self.mapper[k]['type'].items():
                    if tp == 1:
                        color_1.append(self.mapper[k]['type'][tp])
                    else:
                        color_2.append(self.mapper[k]['type'][tp])
        
        return phx, phy, color_1, color_2
                

if __name__ == "__main__":
    
    '''paramateres'''
    no_of_ant = 20
    grid_size = 50
    no_of_food_sources = 2
    food_amount = 50
    iteration = 0
    difusion_rate = 50
    evaporation_rate = 15
    mat = np.zeros((grid_size,grid_size))
    mat2 = np.zeros((grid_size,grid_size))
    
    play = play(grid_size, no_of_food_sources, no_of_ant, difusion_rate, evaporation_rate)
    x,y,sx,sy,grid,board,ants,terminal,loc, mapper= play.initial_state()
    food_counter = {loc[0]:0}
    # food_counter[loc[0]] = 0
    for i in loc[1:]:
        food_counter[i] = food_amount
        
    print(board)
    
    file_name =0 
    while terminal==False:
        # print(food_counter)
        iteration += 1
        start_time = datetime.now()
        
        phx, phy, color_1, color_2 = play.ph_visual()
        file_name += 1
        
        if len(ants) > 0:
            ax, ay = [], []
            for i in ants:
                tempx, tempy = np.where(board == ants[i][1])
                ax.append(tempx[0])
                ay.append(tempy[0])
            
        else:
            ax,ay = x[0], y[0]
        
        fig = plt.figure()  
        axes = plt.gca()
        axes.set_xlim(0, grid)
        axes.set_ylim(0, grid)
        
        nest = axes.plot(x[0],y[0], 'gD') #green for nest
        sources = axes.plot(sx,sy, 'bD') #blue for source
        ants_graph = axes.plot(ax, ay, 'r*') #label=food_counter
        if len(color_1) != 0:
            ph_trace_1 = axes.scatter(phx, phy, c=color_1, cmap="Reds")
            ph_trace = axes.scatter(phx, phy, c=color_2, cmap="Greens")
        # plt.legend(loc="upper right")
        plt.pause(0.02)
        fig.savefig("/home/darshit/Desktop/ELTE SEM 3/SI/Assignment_2/game play/" + str(file_name) + ".jpeg")

        
        ''' looping through all the ants '''
        for ant in range(1,no_of_ant+1):
            if  ants[ant][1] in loc:
                if ants[ant][1] == loc[0]: #at nest
                    if ants[ant][0] == 0: #not carrying food
                        new_loc = play.move(2, ants[ant][1])
                        ants[ant][1] = new_loc
                    else: #carrying food, drop_food
                        food_counter[ants[ant][1]] += 1
                        ants[ant][0] = 0
                else: # at source, pick_food
                    if ants[ant][0] == 0:
                        if food_counter[ants[ant][1]] == 0:
                            del food_counter[ants[ant][1]]
                        else:
                            food_counter[ants[ant][1]] = food_counter[ants[ant][1]] - 1
                            ants[ant][0] = 1
                    else:
                        new_loc = play.move(1, ants[ant][1])
                        ants[ant][1] = new_loc
            
            else:
                if ants[ant][0] == 0: #find food
                    new_loc = play.move(2, ants[ant][1])
                    ants[ant][1] = new_loc
                else: # got to nest
                    new_loc = play.move(1, ants[ant][1])
                    ants[ant][1] = new_loc
                    
        if food_counter[loc[0]] == 1 or len(food_counter) == 1:
            end_time = datetime.now()
            total_sec = end_time - start_time
            total_min = total_sec.seconds/3600
            data = [difusion_rate, evaporation_rate, total_min, food_counter[loc[0]]]
            

            break
    fig.show()