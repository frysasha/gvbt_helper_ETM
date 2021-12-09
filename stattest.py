import numpy
#data = []
#with open(', 'r') as statfile:
#    for line in statfile:
#        data.append([float(x) for x in line.split()])
#        print(data)
#        print(statfile.readlines())
    #array_of_strings = big_file.read().split('\n')

#statfile = open('s')
#array_of_strings = statfile.readlines()
#array_of_strings[0] = '1'

#statmas = [0, 0, 0]

#statfile = open(', 'w')
#lines = statfile.readlines()
#statmas[0] =+ 1
#statmas[2] =- 2
#for line in lines:
#    line = line.strip()
#statfile.writelines(str(statmas))

data = numpy.genfromtxt('text.txt', dtype=int, delimiter=',')
pr = list(data[0])
bl = data[1]
ye = data[2]

pr =+1
print(pr)