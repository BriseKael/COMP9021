#Brise Kael Francis Zoey
import sys
import math
try:
    integer = input('Input a nonnegative integer: ')
    if not integer.isalnum() or int(integer) < 0:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up...')
    sys.exit()
    
num = int(integer)
if num == 0:
    print('Decimal {} reads as {} in factorial base.'.format(integer,0))
elif num == 1:
    print('Decimal {} reads as {} in factorial base.'.format(integer,1))
else:
    i = 0
    while True:
        if num > math.factorial(i):
            i = i + 1
        else:
            break
    an= [0]*(i-1)

    while True:
        if num - math.factorial(i-1) >= 0:
            num = num - math.factorial(i-1)
            an[len(an)-i+1] = an[len(an)-i+1] + 1
        else:
            i = i - 1
        if i < 1:
            break
    print('Decimal {} reads as {} in factorial base.'.format(integer,''.join(str(k) for k in an)))
