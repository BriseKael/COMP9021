## Brise Kael Francis Zoey

import sys

## scan the line form low to high, from left to right
def George(line_list):
    exist_list = list()
    last_sum = 0
    sum1 = 0
    for l in line_list:
        line = [l[1],l[2]]
        if l[3] > 0:
            exist_list.append(line)
        else:
            exist_list.remove(line)
        shadow = sum_George(exist_list)
        sum1 = sum1 + abs(shadow - last_sum)
        last_sum = shadow
    return sum1

## sum the shadow of exist lines
def sum_George(line):
    if len(line) == 0:
        return 0
    _list = list()
    for i in line:
        _list.append(i[0])
        _list.append(i[1])
    _list.sort()
    sum1 = _list[-1] - _list[0]
    for i in range(len(_list)-1):
        templine = (_list[i] + _list[i+1]) / 2
        if not in_George(templine, line):
            sum1 = sum1 - (_list[i+1]-_list[i])
    return sum1

def in_George(a, linerange):
    for line in linerange:
        if a > line[0] and a < line[1]:
            return True
    return False
    
txtname = input('Which data file do you want to use? ')

with open(txtname) as file:
    points_list = [arity.split(' ') for arity in [line.strip() for line in file.readlines()]]

for line in points_list:
    for i in range(4):
        line[i] = int(line[i])
        
##print(points_list)

xline_list = list()
for i in range(len(points_list)):
    ## [x1,y1,x2,y2]
    ## [y1,x1,x2,s] & [y2,x1,x2,s]
    ## s is the state of this line which up-line is -1 and down-line is 1
    xline_list.append([points_list[i][1],points_list[i][0],points_list[i][2],1])
    xline_list.append([points_list[i][3],points_list[i][0],points_list[i][2],-1])
xline_list.sort()
##print(xline_list)

yline_list = list()
for i in range(len(points_list)):
    ## [x1,y1,x2,y2]
    ## [x1,y1,y2,s] & [x2,y1,y2,s]
    ## s is the state of this line which left-line is -1 and down-line is 1
    yline_list.append([points_list[i][0],points_list[i][1],points_list[i][3],1])
    yline_list.append([points_list[i][2],points_list[i][1],points_list[i][3],-1])
yline_list.sort()

print('The perimeter is: {}'.format(George(xline_list)+George(yline_list)))



    
    


