import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
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

def percolation(L,N):
    p1=list(np.linspace(0.1,0.9,15))
    end=[]
    for i in p1:
        koniec=0
        for j in range(N):
            X = fire(L,i)
            if 3 in X[:,L-2]:
                koniec+=1
        print(i)
        end.append(koniec)

    wynik = [x/N for x in end]
    plt.plot(p1,wynik)
    plt.grid()
    plt.xlabel('p')
    plt.title('L={}, MC={}'.format(L-2, N))
    plt.show()


def main():
    L=22
    N=100
    start = time.clock()
    percolation(L,N)
    end = time.clock()
    total = end - start
    print(total)

if __name__=="__main__":
    main()
