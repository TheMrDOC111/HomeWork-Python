import random

f = open('numbers.txt', 'w')
for i in range(500000):
    f.write(str(random.randrange(10000)) + " " + str(random.randrange(1000)) + '\n')
