import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import copy
import time

def fire(L,p,sila,wiatr):
    X  = np.zeros((L+6, L+6))
    X[3:L+3, 3:L+3] = np.random.random(size=(L, L)) < p


    fire=0
    for x in range(3,L+3):
        if X[x, 3] == 1:
            X[x, 3]=2
            fire+=1
    
    while fire>0:
        Y = copy.deepcopy(X)
        for x in range(3,L+3):
            for y in range(3,L+3):
                if Y[x,y] == 0:
                    pass
                elif Y[x,y] == 2:
                    X[x,y] = 3
                    fire-=1
                elif Y[x,y] == 1:
                    if wiatr == '->':
                        if sila == 'slaby':
                            if 2 in [Y[x-1,y-1],Y[x-1,y],Y[x,y-1],Y[x+1,y+1],Y[x+1,y],Y[x,y+1],Y[x+1,y-1],Y[x-1,y+1],Y[x,y-2]]:
                                X[x,y] = 2
                                fire+=1
                        elif sila == 'mocny':
                            if 2 in [Y[x-1,y-1],Y[x-1,y],Y[x,y-1],Y[x+1,y+1],Y[x+1,y],Y[x,y+1],Y[x+1,y-1],Y[x-1,y+1],Y[x,y-2],Y[x,y-3],Y[x+1,y-2],Y[x-1,y-2]]:
                                X[x,y] = 2
                                fire+=1

                    elif wiatr == 'pol':
                        if sila == 'slaby':
                            if 2 in [Y[x-1,y-1],Y[x-1,y],Y[x,y-1],Y[x+1,y+1],Y[x+1,y],Y[x,y+1],Y[x+1,y-1],Y[x-1,y+1],Y[x+2,y]]:
                                X[x,y] = 2
                                fire+=1
                        elif sila == 'mocny':
                            if 2 in [Y[x-1,y-1],Y[x-1,y],Y[x,y-1],Y[x+1,y+1],Y[x+1,y],Y[x,y+1],Y[x+1,y-1],Y[x-1,y+1],Y[x+2,y],Y[x+3,y],Y[x+2,y-1],Y[x+2,y+1]]:
                                X[x,y] = 2
                                fire+=1

                    elif wiatr == '_':
                        if sila == 'slaby':
                            if 2 in [Y[x-1,y-1],Y[x-1,y],Y[x,y-1],Y[x+1,y+1],Y[x+1,y],Y[x,y+1],Y[x+1,y-1],Y[x-1,y+1],Y[x-2,y]]:
                                X[x,y] = 2
                                fire+=1
                        elif sila == 'mocny':
                            if 2 in [Y[x-1,y-1],Y[x-1,y],Y[x,y-1],Y[x+1,y+1],Y[x+1,y],Y[x,y+1],Y[x+1,y-1],Y[x-1,y+1],Y[x-2,y],Y[x-3,y],Y[x-2,y-1],Y[x-2,y+1]]:
                                X[x,y] = 2
                                fire+=1

                    elif wiatr == '<-':
                        if sila == 'slaby':
                            if 2 in [Y[x-1,y-1],Y[x-1,y],Y[x,y-1],Y[x+1,y+1],Y[x+1,y],Y[x,y+1],Y[x+1,y-1],Y[x-1,y+1],Y[x,y+2]]:
                                X[x,y] = 2
                                fire+=1
                        elif sila == 'mocny':
                            if 2 in [Y[x-1,y],Y[x,y-1],Y[x+1,y+1],Y[x+1,y],Y[x,y+1],Y[x-1,y+1],Y[x,y+2],Y[x+1,y+2],Y[x-1,y+2],Y[x,y+3]]:
                                X[x,y] = 2
                                fire+=1
    return X

def cluster(L,X):
    a=np.zeros((L+6,L+6))
    label = 0
    cl = {}
    for x in range(3,L+3):
        for y in range(3,L+3):
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
    p1=list(np.linspace(0.1,0.9,15))
    #p1=0.5
    end=[]
    sila = 'mocny'
    wiatr = '<-'
    for i in p1:
        b=0
        for j in range(N):
            print(j)
            X = fire(L,i,sila,wiatr)
            #X = czysc(L,X)
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
long_cl(100,10)
end = time.clock()
total = end - start
print(total)
