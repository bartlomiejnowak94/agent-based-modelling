import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib import colors
import copy
import imageio

cmap = colors.ListedColormap(['black', 'green'])
L=100
p=0.3
X  = np.zeros((L+6, L+6))
X[3:L+3, 3:L+3] = np.random.random(size=(L, L)) < p

fig = plt.figure(figsize=(7, 7))
im = plt.imshow(X, cmap=cmap)
fig.savefig('obraz0.png')

fire=0
for x in range(3,L+3):
    if X[x, 3] == 1:
        X[x, 3]=2
        fire+=1

cmap = colors.ListedColormap(['black', 'green','red'])
fig = plt.figure(figsize=(7, 7))
im = plt.imshow(X, cmap=cmap)
fig.savefig('obraz1.png')
i=2

#sila = 'slaby'
sila = 'mocny'
#wiatr = '->'
wiatr = '<-'
#wiatr = 'pol'
#wiatr = '_'
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


    cmap = colors.ListedColormap(['black', 'green','red','brown'])
    fig = plt.figure(figsize=(7, 7))
    im = plt.imshow(X, cmap=cmap)
    fig.savefig('obraz{}.png'.format(i))
    i+=1

images = []
for o in range(i):
    images.append(imageio.imread('obraz{}.png'.format(o)))
imageio.mimsave('las.gif', images,'GIF',**{ 'duration': 0.1 }) 
