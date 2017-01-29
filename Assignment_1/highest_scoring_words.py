import sys
      
marks = dict(a=2, b=5, c=4, d=4, e=1, f=6, g=5, h=5, i=1, j=7, k=6, l=3, m=5, n=2, o=3, p=5, q=7, r=2, s=1, t=2, u=4, v=6, w=6, x=7, y=5, z=7)

def getmark(s):
    sum1 = 0
    len1 = len(s)
    for i in range(len1):
        if s[i] == '\'':
            continue
        sum1 = sum1 + marks[s[i]]
    return sum1

def contains(a,b): # if b contains a
    temp = b
    for i in a:
        if i not in temp:
            return False
        else:
            temp = temp.replace(i,'',1)
##    if len(temp) == 0:
####        print('Truely contain')
##        print('The highest score is {}.'.format(getmark(a)))
##        print('The highest scoring word is {}'.format(a))
##        sys.exit()
    return True

term = input('Enter between 3 and 10 lower case letters: ')
term = term.replace(' ', '')
if not term.islower() or not term.isalpha() or len(term)>10 or len(term)<3:
##    print(term.islower(),term.isalpha(),len(term)<=10,len(term)>=3)
    print('Incorrect input, giving up ...')
    sys.exit()

with open('wordsEn.txt') as file:
    dic = file.readlines()
    dic_words = [line.strip() for line in dic]

dic_word_wiout = list()
dic_word_mark = list()
maxmark = 0
result = list()

for line in dic_words:
    if contains(line,term):
        dic_word_wiout.append(line)
        if getmark(line) >= maxmark:
            maxmark = getmark(line)
##            print(maxmark,line)
        dic_word_mark.append(getmark(line))
##print(len(dic_word_wiout),len(dic_word_mark))


for i in range(len(dic_word_wiout)):
    if dic_word_mark[i] == maxmark:
        result.append(dic_word_wiout[i])

if len(result) == 1:
    print('The highest score is {}.'.format(maxmark))
    print('The highest scoring word is {}'.format(result[0]))
elif len(result) == 0:
    print('No word is built from some of those letters. ')
else:
    print('The highest score is {}.'.format(maxmark))
    print('The highest scoring words are, in alphabetical order: ')
    for a in result:
        print('    {}'.format(a))
        

##print(result)
