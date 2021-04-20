import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
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

def percolation(L,N):
    p1=list(np.linspace(0.1,0.9,15))
    end=[]
    sila='mocny'
    wiatr='<-'
    for i in p1:
        koniec=0
        for j in range(N):
            X = fire(L,i,sila,wiatr)
            if 3 in X[:,L+2]:
                koniec+=1
        print(i)
        end.append(koniec)

    wynik = [x/N for x in end]
    plt.plot(p1,wynik)
    plt.grid()
    plt.xlabel('p')
    plt.title('L={}, MC={}, {}, {}'.format(L, N, wiatr, sila))
    plt.show()

#sila = 'slaby'
#sila = 'mocny'
#wiatr = '->'
#wiatr = '<-'
#wiatr = 'pol'
#wiatr = '_'

def main():
    L=20
    N=100
    start = time.clock()
    percolation(L,N)
    end = time.clock()
    total = end - start
    print(total)

if __name__=="__main__":
    main()
