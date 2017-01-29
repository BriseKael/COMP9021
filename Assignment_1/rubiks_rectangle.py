# Brise Kael Francis Zoey
import sys
import math
import copy

class node:
        def __init__(self):
                self.deep = 0
                self.string = list(['']*8)

def cotor(string):
        factorial = [1,1,2,6,24,120,720,5040]
        summation = 0
        for i in range(8):
                times = 0
                for j in range(i+1,8):
                        if (int(string[j]) < int(string[i])):
                                times = times + 1
                summation = summation + times* factorial[7-i]
        return summation

def BFS():
        goal_index = cotor(goal)
        temp = node()
        temp_index = 0
        up = 0
        down = 1
        node_list[up].deep = 0
        node_list[up].string = list('12345678')
        exist_list[cotor(node_list[up].string)] = True
        while exist_list[goal_index] is False:
                temp = copy.deepcopy(node_list[up])
                temp.string.reverse()
                temp_index = cotor(temp.string)
                if not exist_list[temp_index]:
                        exist_list[temp_index] = True
                        node_list[down] = copy.deepcopy(temp)
                        node_list[down].deep = node_list[up].deep + 1
                        down = down + 1
                temp = copy.deepcopy(node_list[up])
                temp.string.insert(0,temp.string.pop(3))
                temp.string.insert(7,temp.string.pop(4))
                temp_index = cotor(temp.string)
                if not exist_list[temp_index]:
                        exist_list[temp_index] = True
                        node_list[down] = copy.deepcopy(temp)
                        node_list[down].deep = node_list[up].deep + 1
                        down = down + 1
                temp = copy.deepcopy(node_list[up])
                temp.string.insert(1,temp.string.pop(6))
                temp.string.insert(5,temp.string.pop(3))
                temp_index = cotor(temp.string)
                if not exist_list[temp_index]:
                        exist_list[temp_index] = True
                        node_list[down] = copy.deepcopy(temp)
                        node_list[down].deep = node_list[up].deep + 1
                        down = down + 1
                up = up + 1
        if node_list[up-1].deep > 0:
                print('{} steps are needed to reach the final configuration.'.format(node_list[up-1].deep+1))
        else:
                print('{} step is needed to reach the final configuration.'.format(node_list[up-1].deep+1))

try:
    goal = input('Input final configuration : ')
    goal = goal.replace(' ', '')
    if not goal.isalnum() or not len(goal) == 8:
            raise ValueError
    alp = list('12345678')
    goal = list(goal)
    for s in goal:
        if alp.count(s) == 0:
            raise ValueError
except ValueError:
    print('Incorrect configuration, giving up...')
    sys.exit()
    
node_list = [node()]*40320
exist_list = [False]*40320

if goal == list('12345678'):
        print('0 step is needed to reach the final configuration.')
        sys.exit()
BFS()

        

                

                
                



    

    



