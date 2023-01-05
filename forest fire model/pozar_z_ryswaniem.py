import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib import colors
import copy
import imageio

cmap = colors.ListedColormap(['black', 'green'])
L=7
p=0.25
X  = np.zeros((L, L))
X[1:L-1, 1:L-1] = np.random.random(size=(L-2, L-2)) < p

fig = plt.figure(figsize=(7, 7))
im = plt.imshow(X, cmap=cmap)
fig.savefig('obraz0.png')

fire=0
for x in range(1,L):
    if X[x, 1] == 1:
        X[x, 1]=2
        fire+=1

cmap = colors.ListedColormap(['black', 'green','red'])
fig = plt.figure(figsize=(7, 7))
im = plt.imshow(X, cmap=cmap)
fig.savefig('obraz1.png')
i=2
while fire>0:
    Y = copy.deepcopy(X)
    for x in range(1,L-1):
        for y in range(1,L-1):
            if Y[x,y] == 0:
                pass
            elif Y[x,y] == 2:
                X[x,y] = 3
                fire-=1
            elif Y[x,y] == 1:
                if 2 in [Y[x-1,y-1],Y[x-1,y],Y[x,y-1],Y[x+1,y+1],Y[x+1,y],Y[x,y+1],Y[x+1,y-1],Y[x-1,y+1]]:
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
