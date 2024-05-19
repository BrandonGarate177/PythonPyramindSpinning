import pygame
from math import * 
import numpy as np
import time 

#we need to create the colors first 

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

#now we need to get the screen going to become a black screen 
#set the width and height of the screen 
WIDTH, HEIGHT = 800, 600
pygame.display.set_caption("This a pyramid that spins ya feel me")
screen = pygame.display.set_mode((WIDTH, HEIGHT)) #set mode iss what actually changes the size of the screem 

scale = 100
angle = 0
#scale is how large we are making stuff, and the angle is the angle that we start on facing our shape 


circle_pos = [WIDTH/2 , HEIGHT/2] # this is the location for the circle posisiotn 
#now we make our pyramids points, 
points = []
# Base of the pyramid (a square)
points.append(np.matrix([-1, -1, 0]))
points.append(np.matrix([1, -1, 0]))
points.append(np.matrix([1, 1, 0]))
points.append(np.matrix([-1, 1, 0]))


# Apex of the pyramid
points.append(np.matrix([0, 0, 2]))
points.append(np.matrix([0, 0, -2]))

#A projection matrix is used to convert 3d cordinates into a visualized 2d plane. 
projection_matrix = np.matrix([
    [1, 0, 0],
    [0, 1, 0]
])

projected_points = [
    [n, n] for n in range(len(points))
]

def connect_points(i, j, points):
    pygame.draw.line(screen, RED, (points[i][0], points[i][1]), (points[j][0], points[j][1]) )


#time to activate our screen to create our window
clock = pygame.time.Clock() #clock so that the animation is even possible 
startTIme = time.time()

#keep track of whether it has been reversed or not 
Reversed = False

while True: 
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

    screen.fill(BLACK)
    #there shall be a whole lot of code inbetween here 
    
    elapsed_time = time.time() - startTIme # this keeps track of how much time has passed  

    if elapsed_time >= 5:
        Reversed = not Reversed
        startTIme = time.time()  # Reset start time

    rotation_factor = -1 if Reversed else 1

    ### this rotates it on the z axis
    rotation_z = np.matrix([
        [cos(angle* rotation_factor), -sin(angle* rotation_factor), 0],
        [sin(angle * rotation_factor), cos(angle* rotation_factor), 0], 
        [0, 0, 1],
    ])
    ### this will rotate on the y axis
    rotation_y = np.matrix([
        [cos(angle * rotation_factor), 0, sin(angle* rotation_factor)], 
        [0,1,0],
        [-sin(angle* rotation_factor), 0, cos(angle * rotation_factor)],
    ])
    ### this will rotate on the x axis
    rotation_x = np.matrix([
        [1, 0, 0], 
        [0, cos(angle* rotation_factor), -sin(angle * rotation_factor)],
        [0, cos(angle * rotation_factor), sin(angle* rotation_factor)],
    ])

    angle +=0.01 # so that the camera angle move, hence the math above 

   



    i = 0
    for point in points:
        rotate2d = np.dot(rotation_z, point.reshape((3,1)))
        rotate2d = np.dot(rotation_y, rotate2d)
        #rotate2d = np.dot(rotation_x, point.reshape((3,1)))
        projected2d = np.dot(projection_matrix, rotate2d)


        # x = int(projected2d[0][0] * scale) + circle_pos[0]
        # y = int(projected2d[1][0] * scale) + circle_pos[1]

        x = int(projected2d[0, 0] * scale) + circle_pos[0]
        y = int(projected2d[1, 0] * scale) + circle_pos[1]

        projected_points[i] = [x, y]
        pygame.draw.circle(screen, WHITE, (x, y), 5)
        i +=1


    for p in range(4):  # There are 4 points in the base
        connect_points(p, (p+1) % 4, projected_points)  # Connect base points
        connect_points(p, 4, projected_points)  # Connect each base point to the apex\
        connect_points(p, 5, projected_points)
    



    pygame.display.update()