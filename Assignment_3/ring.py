## Brise Kael Francis Testarossa Zoey

import math

## This is the most stupid way to achieve this goal--type error.
## It is rough.
## And type(self) must be considered too.

typelist = [type(list()), type(tuple()), type(range(1)), type(str()), type(bytes()), type(bytearray()), type(memoryview(b'kael'))]



class Ring():
    def __init__(self, data = []):
        if type(data) not in typelist and type(data) is not type(self):
            raise TypeError('{} object is not subscriptable'.format(str(type(data))[7:-1]))
        if type(data) is type(self):
            self.data = data.data
        elif type(data) is type(range(1)):
            self.data = list(data)
        else:
            self.data = data
        self.start = 0
        self.step = 1
        self.list = []
        
    def __len__(self):
        return len(self.data)

    def __detachslice(self, index):
        ## length of self.data
        length = len(self)

        ## the first argument of a slice defaults to 0
        if index.start == None:
            start = 0
        else:
            start = index.start % length

        ## the third argument of a slice defaults to 1
        if index.step == None:
            step = 1
        else:
            step = index.step
        ## the second argument of a slice
        if index.stop == None:
            if step >= 0:
                stop = start - 1
            elif step < 0:
                stop = start + 1
        else:
            stop = index.stop
            
        stop = stop % length

        return start, stop, step
    

    def __getslice(self, index):
        length = len(self)
        if index.step == 0:
            ## return empty sequence if step is zero
            if length == 0:
                return self.data
            else:
                return self.data[0:0]
        # do your handling for a slice object:
        start, stop, step = self.__detachslice(index)
        
##        ## used in get slice to make this sequence to be a line.
##        if stop < start:
##            stop += length
##        
##        liststart = self.data[start:start]
##        ## I still think using while is a rough way.
##        ## maybe i could use a.data[slice]+a.data[slice]
##        if step > 0:
##            while start <= stop:
##                temp = start % length
##                liststart += self.data[temp:temp+1]
##                start += step
##        elif step < 0:
##            start += length
##            while start >= stop:
##                temp = start % length
##                liststart += self.data[temp:temp+1]
##                start += step
        if step > 0:
            if stop >= start:
                data = self.data[start:stop+1:step]

            elif stop < start:
                data = self.data[start:]+self.data[:stop+1]
                data = data[::step]
            
        elif step < 0:
            data = self.data[::-1]
            if stop <= start:
                data = data[length-start-1:length-stop:-step]
                
            elif stop > start:
                data = data[length-start-1:]+data[:length-stop]
                data = data[::-step]
        
        return data

    def __getitem__(self, index):
        if type(index) not in [type(int()), type(slice(0))]:
            raise TypeError('ring indices must be integers or slices, not {}'.format(str(type(index))[8:-2]))
        if isinstance(index, slice):
            return self.__getslice(index)
        else:
            index = index % len(self)
            return self.data[index]

    def __setslice(self, index, value):
        length = len(self)
        start, stop, step = self.__detachslice(index)

        ## First, we accept a step of 0, in which case we replace simple slices
        if step == 0:
            if stop >= start:
                self.data[start:stop+1] = value
            elif stop < start:
                temp = self.data[start:start]
                temp[0:0] = value
                self.data = temp+self.data[stop+1:start]
        ## For strictly positive steps, we insert data, between the start and the end
        elif step > 0:
            if stop <= start:
                stop += length
            if math.ceil((stop-start)/step) != len(value):
                raise ValueError('attempt to insert sequence of size {} to extended slice of size {}'.format(len(value), math.ceil((stop-start)/step)))
            index = 0
            for ele in value:
                if start+index+1 >= len(self):
                    start, index = 0, -1
                right = self.data[(start+index+1):]
                left = self.data[:(start+index+1)]
                temp = self.data[0:0]
                temp.append(ele)
                self.data = left+temp+right
                index += 1
                start += step
        elif step < 0:
            if stop <= start:
                stop += length
            if math.ceil((stop-start+1)/-step) != len(value):
                raise ValueError('attempt to replace sequence of size {} to extended slice of size {}'.format(len(value), math.ceil((stop-start+1)/-step)))
            for ele in value:
                self.data[start%length] = ele
                start -= step

    
    def __setitem__(self, index, value):
        if type(index) not in [type(int()), type(slice(0))]:
            raise TypeError('ring indices must be integers or slices, not {}'.format(str(type(index))[8:-2]))
        if isinstance(index, slice):
            return self.__setslice(index, value)
        else:
            index = index % len(self)
            self.data[index] = value

    def __eq__(self, obj):
        return self.data == obj.data

    def __iter__(self):
        return self

    def __next__(self):
        temp = self[self.start]
        if temp in self.list:
            self.list = []
            raise StopIteration
        else:
            self.list.append(temp)
            self.start += self.step
            return temp

    def __repr__(self):
        return 'Ring({})'.format(self.data)

    def __str__(self):
        return '{}'.format(self.data)

##b = list(range(10))
##a = Ring(b)
##a = Ring([1,2,3,4,5])
##
