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

def cluster(L,X):
    a=np.zeros((L,L))
    label = 0
    cl = {}
    for x in range(1,L-1):
        for y in range(1,L-1):
            if X[x,y] == 3:
                left = X[x,y-1]
                above = X[x-1,y]
                if left == 0 and above == 0:
                    label += 1
                    a[x,y]=label
                    cl[label]=[(x,y)]

                elif left != 0 and above == 0:
                    a[x,y]=a[x,y-1]
                    cl[a[x,y-1]].append((x,y))

                elif left == 0 and above != 0:
                    a[x,y]=a[x-1,y]
                    cl[a[x-1,y]].append((x,y))

                else:
                    low = min(a[x,y-1],a[x-1,y])
                    high = max(a[x,y-1],a[x-1,y])
                    a[x,y] = low
                    cl[low].append((x,y))

                    if low!=high:
                        for i in cl[high]:
                            a[i[0],i[1]] = low
                            cl[low].append((i[0],i[1]))
                        cl.pop(high)
    return X,cl

def long_cl(L,N):
    p1=list(np.linspace(0.1,1,20))
    #p1=0.5
    end=[]
    for i in p1:
        b=0
        for j in range(N):
            print(j)
            X = fire(L,i)
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
long_cl(102,10)
end = time.clock()
total = end - start
print(total)
