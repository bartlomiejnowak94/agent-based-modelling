import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import copy
import time

def fire(L,p):
    X  = np.zeros((L, L))
    X[1:L-1, 1:L-1] = np.random.random(size=(L-2, L-2)) < p

    fire=0
    for x in range(1,L):
        if X[x, 1] == 1:
            X[x, 1]=2
            fire+=1

    i=2
    while fire>0:
        Y = copy.deepcopy(X)
        for x in range(1,L-1):
            for y in range(1,L-1):
                if Y[x,y] == 2:
                    X[x,y] = 3
                    fire-=1
                elif Y[x,y] == 1:
                    if 2 in [Y[x-1,y-1],Y[x-1,y],Y[x,y-1],Y[x+1,y+1],Y[x+1,y],Y[x,y+1],Y[x+1,y-1],Y[x-1,y+1]]:
                        X[x,y] = 2
                        fire+=1
    return X

def czysc(L,X):
    #change values: 0 - burned tree, -1 - tree or empty
    for x in range(0,L):
        for y in range(0,L):
            if X[x,y] == 3:
                X[x,y] = 0
            elif X[x,y] == 1:
                X[x,y] = -1
            elif X[x,y] == 0:
                X[x,y] = -1
    return X


def cluster(L,X):
    label = 0
    cl = {1:[]}
    for x in range(1,L-1):
        for y in range(1,L-1):
            if X[x,y] == 0:
                if X[x-1,y]<1 and X[x,y-1]<1:
                    label += 1
                    X[x,y]=label
                    cl[label]=[(x,y)]

                elif X[x,y-1]>=1 and X[x-1,y]<1:
                    X[x,y]=X[x,y-1]
                    cl[X[x,y-1]].append((x,y))

                elif X[x,y-1]<1 and X[x-1,y]>=1:
                    X[x,y]=X[x-1,y]
                    cl[X[x-1,y]].append((x,y))

                elif X[x-1,y]>=1 and X[x,y-1]>=1:
                    low = min(X[x,y-1],X[x-1,y])
                    high = max(X[x,y-1],X[x-1,y])
                    X[x,y] = low
                    cl[low].append((x,y))

                    if low!=high:
                        for i in cl[high]:
                            X[i[0],i[1]] = low
                            cl[low].append((i[0],i[1]))
                        cl.pop(high)
##                    if X[x-1,y] == X[x,y-1]:
##                        X[x,y]=X[x-1,y]
##                        cl[X[x-1,y]].append((x,y))
##                    elif X[x-1,y] > X[x,y-1]:
##                        X[x,y]=X[x,y-1]
##                        cl[X[x,y-1]].append((x,y))
##                        for i in cl[X[x-1,y]]:
##                            X[i[0],i[1]]=X[x,y-1]
##                            cl[X[x,y-1]].append((i[0],i[1]))
##                        cl.pop(X[x-1,y])
##                    elif X[x-1,y] < X[x,y-1]:
##                        X[x,y]=X[x-1,y]
##                        cl[X[x-1,y]].append((x,y))
##                        for i in cl[X[x,y-1]]:
##                            X[i[0],i[1]]=X[x-1,y]
##                            cl[X[x-1,y]].append((i[0],i[1]))
##                        cl.pop(X[x,y-1])


    return X,cl

def long_cl(L,N):
    p1=list(np.linspace(0.1,0.9,15))
    #p1=0.5
    end=[]
    for i in p1:
        b=0
        for j in range(N):
            print(j)
            X = fire(L,i)
            X = czysc(L,X)
            X,cl = cluster(L,X)
            b+=max(len(v) for v in cl.values())
        print(i)
        end.append(b/N)

    wynik = end
    plt.plot(p1,wynik)
    plt.grid()
    plt.xlabel('p')
    plt.title('MC={}'.format(N))
    plt.show()
                           
                                


start = time.clock()
long_cl(102,50)
end = time.clock()
total = end - start
print(total)
