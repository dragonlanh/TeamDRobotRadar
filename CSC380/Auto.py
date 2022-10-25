from re import X
from time import sleep
import pygame

pygame.init()
clock = pygame.time.Clock()
pygame.key.set_repeat(20, 20)
screensize = (500, 500)
scene = pygame.display.set_mode(screensize)


robotBody = pygame.image.load("kermit.png")
robotRect = robotBody.get_rect()

groundSprite = pygame.image.load('floor.jpg')

robotX = 225
robotY = 225


def robot(x, y):
    scene.blit(robotBody, (x, y))
    global robotX, robotY
    robotX = x
    robotY = y

def robotControl(left, down, right, up):
    global robotX, robotY
    speed = 5
    robotX += speed*left
    robotX += speed*right
    robotY -= speed*down
    robotY -= speed*up


def surface(x, y):
    scene.blit(groundSprite, (x, y))


starting = True
while starting:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            starting = False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            print(pos)
            
            while pos[0] > robotX:
                robotX += .1
                robot(robotX, robotY)
                pygame.display.flip()
                for i in range(0, 500, 64):
                    for j in range(0, 500, 64):
                        surface(i, j)

                
            while pos[0] < robotX:
                robotX -= .1
                robot(robotX, robotY)
                pygame.display.flip()
                for i in range(0, 500, 64):
                    for j in range(0, 500, 64):
                        surface(i, j)
                
            while pos[1] < robotY:
                robotY -= .1
                robot(robotX, robotY)
                pygame.display.flip()
                for i in range(0, 500, 64):
                    for j in range(0, 500, 64):
                        surface(i, j)
                        
            while pos[1] > robotY:
                robotY += .1
                robot(robotX, robotY)
                pygame.display.flip()
                for i in range(0, 500, 64):
                    for j in range(0, 500, 64):
                        surface(i, j)

    for i in range(0, 500, 64):
        for j in range(0, 500, 64):
            surface(i, j)

    robot(robotX, robotY)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()