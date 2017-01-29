## Brise Kael Francis Testarossa Zoey

## 2016-05-08 assignment2
import math

## The stuctures are Graph and Point.
## Every Graph has a pointlist which contains points, color, linelist and vectorlist.
## Every Point has a x, y. And angle and side.

class point:
    def __init__(self):
        self.x = None
        self.y = None

        self.angle = None
        self.side = None
        
    def __repr__(self):
        return '[{}, {}]'.format(self.x, self.y)
        

class graph:
    def __init__(self, pointlist = None, color = None):
        self.pointlist = list()
        self.color = None

        self.linelist = list()
        self.vectorlist = list()


    def generateline(self):
        if self.pointlist:
            for i in range(-1, len(self.pointlist)-1):
                self.linelist.append([[self.pointlist[i].x, self.pointlist[i].y], [self.pointlist[i+1].x, self.pointlist[i+1].y]])

    def generatevector(self):
        if self.linelist:
            for i in range(-1, len(self.linelist)-1):
                self.vectorlist.append([self.pointlist[i+1].x-self.pointlist[i].x, self.pointlist[i+1].y-self.pointlist[i].y])

    def check_convex(self):
## This part is to check whether it is a closed graph
        total_vector = [0,0]
        for vector in self.vectorlist:
            total_vector[0] += vector[0]
            total_vector[1] += vector[1]
        if total_vector != [0, 0]:
            return False
## This part calculate the sum of angles. Convex polygon: sum of the angle is (side-2)*180
## If there are some errors, there must be some case which this graph is not a polygon.
        angle_sum = list()
        for i in range(-1, len(self.vectorlist)-1):
            try:
                cosA = (0-self.vectorlist[i][0]*self.vectorlist[i+1][0]-self.vectorlist[i][1]*self.vectorlist[i+1][1]) /\
                       math.sqrt((self.vectorlist[i][0]**2+self.vectorlist[i][1]**2)*(self.vectorlist[i+1][0]**2+self.vectorlist[i+1][1]**2))
                angleA = math.acos(cosA)*180/math.pi
                self.pointlist[i].angle = round(angleA, 2)
                self.pointlist[i].side = round(math.sqrt((self.vectorlist[i][0]**2+self.vectorlist[i][1]**2)*(self.vectorlist[i+1][0]**2+self.vectorlist[i+1][1]**2)), 2)
                angle_sum.append(angleA)
            except:
                return False
## '1' is the deviation.
        if abs(sum(angle_sum) - (len(self.pointlist)-2)*180) > 1:
            return False
        
        return True

## Reading xml files.
## For each line, if 'svg' in it, then jump this first line of xml. 
## If M and L in this line. add point value to point_temp. Then jump.
## If fill in this line, add color to graph_temp. Then jump.
## If this line is too short, which means it may be not a line contains the correct value. Then drop it.
## Calculate the line and vectors of this graph. It would be useful for following steps.
## Add this graph_temp to graphlist.
def available_coloured_pieces(file):
    filedata = file.readlines()
    fileline = [line.strip() for line in filedata]
    pointlist = list()
    graphlist = list()

    for ele in fileline:
        if 'svg' in ele:
            continue
        line = ele[8:-2].split()
##        print(line)
        graph_temp = graph()
        for i in range(len(line)):
            point_temp = point()
            if 'M' in line[i] or 'L' in line[i]:
                point_temp.x = float(line[i+1])
                point_temp.y = float(line[i+2])
                graph_temp.pointlist.append(point_temp)
                continue
            if 'fill' in line[i]:
                graph_temp.color = line[i][6:-1]
                continue
        if len(graph_temp.pointlist) < 3:
            continue
        graph_temp.generateline() ##############
        graph_temp.generatevector() ######
        graphlist.append(graph_temp)
    return graphlist


## For each graph in graphlist, check the convex.
def are_valid(graphlist):
    for ele in graphlist:
        if ele.check_convex() == False:
            return False

    return True

## Compare with graphlist1 and graphlist2, if they are not valid, return false.
## Setup a dictionary with color in key and graphlist in value.
## If key numbers don't match, then return False.
## Temp1 is one order of graph from graphlist1.
## Temp2 and temp2.reverse() are possible order of graph from graphlist2
## Temp3 and temp3.reverse() are possible order of reversed graph from graphlist2.
## If any possible order can match temp1. Then ok is not 0 and we don't need to return False.
def are_identical_sets_of_coloured_pieces(graphlist1, graphlist2):
    if not are_valid(graphlist1) or not are_valid(graphlist2):
        return False
    graphdic1 = dict()
    graphdic2 = dict()
    for ele in graphlist1:
        graphdic1[ele.color] = ele
    for ele in graphlist2:
        graphdic2[ele.color] = ele
    if graphdic1.keys() != graphdic2.keys():
        return False
    for key in graphdic1.keys():
        temp1, temp2, temp3 = list(), list(), list()
        for i in range(len(graphdic1[key].pointlist)):
            temp1.append([graphdic1[key].pointlist[i].angle, graphdic1[key].pointlist[i].side])
            temp2.append([graphdic2[key].pointlist[i].angle, graphdic2[key].pointlist[i].side])
            temp3.append([graphdic2[key].pointlist[i].angle, graphdic2[key].pointlist[i-1].side])

        ok = 0       
        for i in range(len(temp1)):
            if temp2[i] == temp1[0] and temp2[i:]+temp2[:i] == temp1:
                ok += 1
            temp2.reverse()
            if temp2[i] == temp1[0] and temp2[i:]+temp2[:i] == temp1:
                ok += 1
            if temp3[i] == temp1[0] and temp3[i:]+temp3[:i] == temp1:
                ok += 1
            temp3.reverse()
            if temp3[i] == temp1[0] and temp3[i:]+temp3[:i] == temp1:
                ok += 1
        if ok == 0:
            return False
    return True

## This is the function to check if test point is in the list of vert or not.
## Vert is a list of points. can be seen as a graph.
## 0.01 is the deviation of checking point is on the side.
## If c%2 is 0, means it must be out of the graph. If return 1, it means test point is on the side or in the graph.
def pnpoly(vert, test):
    c = 0
    for i in range(len(vert)):
        AB = math.hypot(vert[i-1][0]-vert[i][0], vert[i-1][1]-vert[i][1])
        BC = math.hypot(test[0]-vert[i][0], test[1]-vert[i][1])
        AC = math.hypot(test[0]-vert[i-1][0], test[1]-vert[i-1][1])

        if AC + BC - AB <= 0.01:
            return 1
        if ((vert[i][1] > test[1]) != (vert[i-1][1] > test[1])) and (test[0] < ((vert[i-1][0]-vert[i][0])*(test[1]-vert[i][1])/\
                                                     (vert[i-1][1]-vert[i][1])+vert[i][0])):
            c += 1
    return c%2


## This part is to calculate the area of the graphs in one list.
## However, I think this part may not work on Q3.
def area(graphlist):
    summ = 0
    for graph in graphlist:
        tempsum = 0
        for i in range(len(graph.pointlist)):
            dx1 = graph.pointlist[i-1].x
            dy1 = graph.pointlist[i-1].y
            dx2 = graph.pointlist[i].x
            dy2 = graph.pointlist[i].y
            tempsum += (dx1*dy2-dy1*dx2)/2
        summ += abs(tempsum)
    return abs(summ)

## This part is to see if the graphlist has one graph that is cross another graph.
## The way is to check each line of the graph comparing with the other lines of other graphs.
## If the cross point is one of the endpoint, jump this case by continue.
def linecross(graphlist):
    total_linelist = list()
    for graph in graphlist:
        total_linelist.extend(graph.linelist)
    for graph in graphlist:
        for line in graph.linelist:
            for targetline in total_linelist:
                if line == targetline:
                    continue
                d = (line[1][1]-line[0][1])*(targetline[1][0]-targetline[0][0])-\
                    (targetline[1][1]-targetline[0][1])*(line[1][0]-line[0][0])
                if d == 0:
                    continue
                x = [0, 0]
                x[0] = ((line[1][0]-line[0][0])*(targetline[1][0]-targetline[0][0])*(targetline[0][1]-line[0][1])+\
                      (line[1][1]-line[0][1])*(targetline[1][0]-targetline[0][0])*line[0][0]-\
                      (targetline[1][1]-targetline[0][1])*(line[1][0]-line[0][0])*targetline[0][0])/d
                x[1] = ((line[1][1]-line[0][1])*(targetline[1][1]-targetline[0][1])*(targetline[0][0]-line[0][0])+\
                      (line[1][0]-line[0][0])*(targetline[1][1]-targetline[0][1])*line[0][1]-\
                      (targetline[1][0]-targetline[0][0])*(line[1][1]-line[0][1])*targetline[0][1])/(-d)
                if (x[0]-line[0][0])*(x[0]-line[1][0]) < 0 and \
                   (x[0]-targetline[0][0])*(x[0]-targetline[1][0]) < 0 and \
                   (x[1]-line[0][1])*(x[1]-line[1][1]) < 0 and \
                   (x[1]-targetline[0][1])*(x[1]-targetline[1][1]) < 0:
                    return False
    return True
                
            
        
## First, calculate the area of each graph of graphlist and the targetlist.
## Second, check if the graphlist has the valid graph.
## Third, check the graphlist has no case of crossing graphs.
## Finally, check each points of graph from graphlist are in the targetlist.
## If every points are in the target graph. Well done, which I think it is a solution.
def is_solution(graphlist, targetlist):
    if area(graphlist) != area(targetlist):
##        print('1')
        return False
    if are_valid(graphlist) == False:
        return False
    if linecross(graphlist) == False:
        return False
    vert = list()
    for point in targetlist[0].pointlist:
        vert.append([point.x, point.y])

    for graph in graphlist:

        for point in graph.pointlist:

            if pnpoly(vert, [point.x, point.y]) == 0:
##                print('2')
                return False
    
    return True

## Brise Kael Francis Testarossa Zoey
## 2016-06 Assignment3

## This time, I realized I need to figure out something new like a new class to store my shapes.
## Which is digitalization.

Letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
Directions = '→←↑↓↘︎↗︎↖︎↙︎'

class vector_edge:
    def __init__(self):
        self.start = None
        self.direction = None
        self.end = None
        self.length = None
    def __repr__(self):
        return '\n ({}, {})'.format(self.direction, self.length)
    

class vector_graph:
    def __init__(self):
        self.pointlist = list()
        
        self.mainpoint = None
        self.edgelist = list()
        self.color = None

        self.height = None
        self.width = None
        
        self.digital_list = list()
        

    def __repr__(self):
        return 'Vector_graph: {}, {}, [{}, {}] \n'.format(self.color, self.edgelist, self.width, self.height)


def vector(graph_list):
    vector_graph_list = list()
    for graph in graph_list:
        temp_graph = vector_graph()
        temp_graph.color = graph.color
        temp_graph.pointlist = graph.pointlist
        i = 0
        for vector in graph.vectorlist:
            temp_edge = vector_edge()
            temp_edge.start = Letters[i]
            temp_edge.direction = ''
            if vector[0] != 0:
                if vector[0] > 0:
                    temp_edge.direction += Directions[0]
                else:
                    temp_edge.direction += Directions[1]                    
            if vector[1] != 0:
                if vector[1] > 0:
                    temp_edge.direction += Directions[2]
                else:
                    temp_edge.direction += Directions[3]
            temp_edge.end = Letters[i+1]
            if i+1 == len(graph.vectorlist):
                temp_edge.end = Letters[0]
            temp_edge.length = int(max(abs(vector[0]), abs(vector[1])))
            temp_graph.edgelist.append(temp_edge)
            i += 1

        width, height = 0, 0
        widthset, heightset = set(), set()
        for edge in temp_graph.edgelist:
            if '→' in edge.direction:
                width += edge.length
            elif '←' in edge.direction:
                width -= edge.length
            if '↑' in edge.direction:
                height += edge.length
            elif '↓' in edge.direction:
                height -= edge.length
            widthset.add(abs(width))
            heightset.add(abs(height))

        temp_graph.width = max(widthset)
        temp_graph.height = max(heightset)
        vector_graph_list.append(temp_graph)
    return vector_graph_list


def digital(vector_graph_list, shape_list):
    lengths = set()
    for graph in vector_graph_list:
        for edge in graph.edgelist:
            lengths.add(edge.length)
    lengths = list(lengths)
    print(lengths)
    gcd = list()
    for i in range(len(lengths)):
        gcd.append(math.gcd(lengths[i-1], lengths[i]))
    print(min(gcd), gcd)

    biaozhun = min(gcd)

    shape = shape_list[0]
    shape.width = shape.width // biaozhun
    shape.height = shape.height // biaozhun
        
    for shape_edge in shape.edgelist:
        shape_edge.length = shape_edge.length // biaozhun

    xset, yset = set(), set()
    for shape_point in shape.pointlist:
        xset.add(shape_point.x)
        yset.add(shape_point.y)
    dx = min(xset)
    dy = min(yset)
    for shape_point in shape.pointlist:
        shape_point.x -= dx
        shape_point.y -= dy
        shape_point.x = shape_point.x // biaozhun
        shape_point.y = shape_point.y // biaozhun

    
    for graph in vector_graph_list:
        graph.width = graph.width // biaozhun
        graph.height = graph.height // biaozhun
        for edge in graph.edgelist:
            edge.length = edge.length // biaozhun

        xset, yset = set(), set()
        for graph_point in graph.pointlist:
            xset.add(graph_point.x)
            yset.add(graph_point.y)
        dx, dy = min(xset), min(yset)
        for graph_point in graph.pointlist:
            graph_point.x -= dx
            graph_point.y -= dy
            graph_point.x = graph_point.x // biaozhun
            graph_point.y = graph_point.y // biaozhun
    


        
    

    
    pass



##file = open('pieces_A.xml')
##this = available_coloured_pieces(file)
##that = vector(this)
##
##file = open('shape_A_1.xml')
##shape = available_coloured_pieces(file)
##shape = vector(shape)
##
##digital(that, shape)




































