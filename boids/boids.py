import pygame, sys
from pygame.math import Vector2
from pygame.locals import *
import random as rnd
from math import *

# Program requires pygame. After procesing this program on blue screen please clik left mouse key to spam boids, and right clik to spam obstalces.
# Warning: Too much boids and obstacles can slow displaying game. 


###########################################
#  Class Boid
###########################################

class Boid:
    def __init__(self, screen , position):
        self.screen = screen
        self.position = position #position of mouse on screen
        self.pos = Vector2(position[0], position[1]) #positions of boid is vector which reads x and y from mouse position
        self.vel = Vector2(rnd.uniform(-3,3), rnd.uniform(-3,3)) #velocity is vector which have vx and vy component from (-3,3) period

    #method to move boid
    def move(self): 
        self.pos += self.vel #add velocity to position
        self.pos = Vector2(self.pos.x%1000,self.pos.y%800) #after break boundaries update positions to make periodic boundary conditions

    #method to draw boid
    def draw(self): 
        points = [Vector2(0,7), Vector2(2,2), Vector2(-2,2)]
        # rotate points
        angle = self.vel.angle_to(Vector2(0,1))
        points = [p.rotate(angle) for p in points]
        # fix y axis
        points = [Vector2(p.x*-1,p.y) for p in points]
        # add current position
        points = [self.pos+p*2 for p in points]
        pygame.draw.polygon(screen, (0, 0, 0), points)

    #method to draw obstacle which is in fact boid, but with another shape, and which doesn't move
    def draw_obst(self):
        pygame.draw.rect(screen, RED, pygame.Rect((self.pos.x - 20, self.pos.y - 20), (40,40))) #create rectangle

###########################################
#  Definitions for neighboorhood
###########################################

def neigh(boid,other,d): #check if other boid is neighbor of our boid. It means other is inside of circle with radius d
    if sqrt((other.pos.x - boid.pos.x)**2 + (other.pos.y - boid.pos.y)**2) < d:
        return True
    else:
        return False

def neilist_b(boid,boidlist,d):
    neilist = {}
    vel_x = []
    vel_y = []
    positions = []
    for i in boidlist: #for all boids in boidlist
        if i != boid: #if he is not himself
            if neigh(boid,i,d) == True: #and is boid's neighbor 
                neilist[(i.pos.x,i.pos.y)] = (i.vel.x,i.vel.y) #add his positions and velocities to dictionary
                vel_x.append(i.vel.x) #add his vx to list
                vel_y.append(i.vel.y) #add his vy to list
                positions.append((i.pos.x,i.pos.y)) #add his position to list
                
    return neilist, vel_x, vel_y, positions

###########################################
#  Change velocieties, alignment
###########################################

####### ALIGNMENT #######
def change_vel(boid,d,weight,boidlist):
    neis, vel_x, vel_y, posi = neilist_b(boid,boidlist,d) #take all neighbors for boid
    if len(neis) != 0:
        boid.vel.x = boid.vel.x + (weight*((sum(vel_x)/len(vel_x))-boid.vel.x)) #if boid have at least 1 neighbor align his velocity on x (to do this i use means of vx and vy of neighbors)
        boid.vel.y = boid.vel.y + (weight*((sum(vel_y)/len(vel_y))-boid.vel.y)) #the same on y
    else: #else leave velocities 
        boid.vel.x = boid.vel.x
        boid.vel.y = boid.vel.y

def go_to_middle(boid,weight2,weight3,boidlist,minimal,d):
    neis, vel_x, vel_y, posi = neilist_b(boid,boidlist,d) #again take all neighbors
    dl_all = {}
    if len(posi) != 0: #if boid have at least 1 neighbor 
        for i in posi: #take positions of neighbors
            dl = sqrt((i[0] - boid.pos.x)**2 + (i[1] - boid.pos.y)**2) #calculate distances
            dl_all[i] = dl #and put them into dictionary
        all_neis = list(dl_all.values()) #take all distances
        dl_mean = sum(all_neis)/len(all_neis) #calclulate mean 
        for i in posi:
            ####### COHESION #######
            if dl_all[i] >= minimal:  #if distance to other boid is larger than minimal i change boid's velocity with weight =  weigh2
                boid.vel.x = boid.vel.x + weight2*((i[0] - boid.pos.x)*(dl_all[i] - dl_mean)/dl_all[i])
                boid.vel.y = boid.vel.y + weight2*((i[1] - boid.pos.y)*(dl_all[i] - dl_mean)/dl_all[i])
            ####### SEPARATION #######  
            elif dl_all[i] < minimal: #if distance is too close i must push boid away from neighbor
                boid.vel.x = boid.vel.x - weight3*(((i[0] - boid.pos.x)*minimal/dl_all[i])-(i[0] - boid.pos.x)) #to do this i change its velocity on x
                boid.vel.y = boid.vel.y - weight3*(((i[1] - boid.pos.y)*minimal/dl_all[i])-(i[1] - boid.pos.y)) #and y

####### AVOIDING OBSTACLES #######
def avoid_obst(boid, obstacles,d):
    if len(obstacles) > 0:
        for obst in obstacles: #for obstacles in list names obstacles
            dl= sqrt((boid.pos.x - obst.pos.x)**2 + (boid.pos.y - obst.pos.y)**2) #i calculate distance
            if dl <= 50: #if boid is to close obstacle
                boid.vel.x = boid.vel.x - 0.1*(((obst.pos.x - boid.pos.x)*50/dl)-(obst.pos.x - boid.pos.x)) #change boid's velocity to push him away
                boid.vel.y = boid.vel.y - 0.1*(((obst.pos.y - boid.pos.y)*50/dl)-(obst.pos.y - boid.pos.y))
            else: #if boid is in good distance don't change velocity
                boid.vel.x = boid.vel.x
                boid.vel.y = boid.vel.y
                
###########################################
#  Slow to fast boids and move stop boids
###########################################

def slow_me(boid,max_speed, max_speed2): 
    if boid.vel.x >= max_speed: #if boid have more than maximum speed slow him down
        boid.vel.x = boid.vel.x - 1
    elif boid.vel.x <= max_speed2: #in both directions. Eg. We have maximum speed equals to 3. If speed on x is -4 we must change it to -3 or if speed on x is 4 we must change it to 3 
        boid.vel.x = boid.vel.x + 1

    if boid.vel.y >= max_speed: #i do the same for y component of velocity
        boid.vel.y = boid.vel.y - 1
    elif boid.vel.y <= max_speed2:
        boid.vel.y = boid.vel.y + 1

def move_me(boid): 
    if boid.vel.x == 0 and boid.vel.y == 0: #Sometimes boid can stop because avoiding obstacles and 3 rules of moving can change velocity to 0.
        boid.vel.x = boid.vel.x + 2 #So i increase speed of boid if he stops. Smth like awakening
        boid.vel.y = boid.vel.y + 2

###########################################
#  Pygame interface and uses
###########################################

pygame.init() #initialization of pygmae
screen = pygame.display.set_mode((1000,800),0,32) #create screen for game
pygame.display.set_caption('Birds on sky - left clik to create boid; right click to create obstacle') #title
WHITE = (255, 255, 255) #some colors to use
BLUE = (0, 0, 255)
RED = (255, 0, 0)
SKYBLUE = (135,206,235)
BLACK = (0,0,0)
FPS = 30 #frames per second
fpsClock = pygame.time.Clock() #start clock to count game time
boidlist = [] #inicialization for boid list
obstacles = [] #and obstacles list
d = 40 #radius of boid's view
weight = 0.3 #weight of alignment
weight2 = 0.3 #weight of cohesion
weight3 = 0.3 #weight of separation
minimal = 10 #minimal distance to another boids
max_speed = 3 #maximum speeds
max_speed2 = -3


while True: #game ends when we close it
    for boid in boidlist: #for all boids
        if len(boidlist) > 0: #if we have boids
            change_vel(boid,d,weight,boidlist) #align boid to anothers
            go_to_middle(boid,weight2,weight3,boidlist,minimal,d) #move to middle of mass and move avay of anothers if boid is too close
            avoid_obst(boid, obstacles,d) #avoid all obstacles
            slow_me(boid,max_speed,max_speed2) #slow me if u need
            move_me(boid) #give me bigger velocity when i stop
        boid.move() #move boids
        
    screen.fill(SKYBLUE) #fill screan with color
    for boid in boidlist: #draw all boids
        boid.draw()
    for obst in obstacles: #draw all obstacles
        obst.draw_obst()
    pygame.display.update() #update screen
    fpsClock.tick(FPS) #count clock including FPS
    for event in pygame.event.get(): #loop which check events of our game
        if event.type == QUIT: #if we click 'x' in top-right screen game close
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONUP and event.button == 1: #if we click left mouse key boid appers on mouse position
            boidlist.append(Boid(screen, event.pos))
        elif event.type == MOUSEBUTTONUP and event.button == 3: #if we click right obstacle appers on mouse position
            obstacles.append(Boid(screen, event.pos)) #obstalce is boid but we distinguish them by adding obstales to another list