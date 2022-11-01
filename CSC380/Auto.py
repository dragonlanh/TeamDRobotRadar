from re import X
from time import sleep
import pygame
import requests

pygame.init()
clock = pygame.time.Clock()
pygame.key.set_repeat(20, 20)
screensize = (500, 500)
scene = pygame.display.set_mode(screensize)
currentMovement = "none"
turned = False
facing = "up"

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

def faceRight():
    if facing == "up":
        UpdateCurrentMovement("right")
    if facing == "left":
        UpdateCurrentMovement("180")
    if facing == "down":
        UpdateCurrentMovement("left")
    facing == "right"

def faceUp():
    if facing == "right":
        UpdateCurrentMovement("left")
    if facing == "left":
        UpdateCurrentMovement("right")
    if facing == "down":
        UpdateCurrentMovement("180")
    facing == "up"

def faceLeft():
    if facing == "up":
        UpdateCurrentMovement("left")
    if facing == "right":
        UpdateCurrentMovement("180")
    if facing == "down":
        UpdateCurrentMovement("right")
    facing == "left"

def faceDown():
    if facing == "up":
        UpdateCurrentMovement("180")
    if facing == "left":
        UpdateCurrentMovement("left")
    if facing == "right":
        UpdateCurrentMovement("right")
    facing == "down"

def surface(x, y):
    scene.blit(groundSprite, (x, y))

def ChangeMovementMode(mode):
    if mode == "remote":
        res = requests.get("http://192.168.1.130:8080/ChangeMoveMode/remote")
        print(res)
    elif mode == "auto":
        res = requests.get("http://192.168.1.130:8080/ChangeMoveMode/auto")
        print(res)
    elif mode == "roam":
        res = requests.get("http://192.168.1.130:8080/ChangeMoveMode/roam")
        print(res)
    elif mode == "idle":
        res = requests.get("http://192.168.1.130:8080/ChangeMoveMode/idle")
        print(res)
    else:
        print("error, mode not accepted")

def SendMovement(movement):
    try:
        res = requests.get(f"http://192.168.1.130:8080/MovementPress/{movement}", timeout=0.01)
        print(res)
    except requests.exceptions.Timeout as err:
        pass

def UpdateCurrentMovement(movement):
    if movement != currentMovement:
        SendMovement(movement)
        return movement
    return movement

starting = True
while starting:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            starting = False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            print(pos)
            
            #right
            while (pos[0] - 50) > robotX:
                if facing != "right" and turned == False:
                    faceRight()
                    turned == True
                UpdateCurrentMovement("fwd")
                robotX += .5
                robot(robotX, robotY)
                pygame.display.flip()
                for i in range(0, 500, 64):
                    for j in range(0, 500, 64):
                        surface(i, j)

            turned == False
            
            #left
            while (pos[0] - 50) < robotX:
                if facing != "left" and turned == False:
                    faceLeft()
                    turned == True
                UpdateCurrentMovement("fwd")
                robotX -= .5
                robot(robotX, robotY)
                pygame.display.flip()
                for i in range(0, 500, 64):
                    for j in range(0, 500, 64):
                        surface(i, j)

            turned == False
            
            #up
            while (pos[1] - 50) < robotY:
                if facing != "up" and turned == False:
                    faceUp()
                    turned == True
                UpdateCurrentMovement("fwd")
                robotY -= .5
                robot(robotX, robotY)
                pygame.display.flip()
                for i in range(0, 500, 64):
                    for j in range(0, 500, 64):
                        surface(i, j)

            turned == False
            
            #down
            while (pos[1] - 50) > robotY:
                if facing != "down" and turned == False:
                    faceDown()
                    turned == True
                UpdateCurrentMovement("fwd")
                robotY += .5
                robot(robotX, robotY)
                pygame.display.flip()
                for i in range(0, 500, 64):
                    for j in range(0, 500, 64):
                        surface(i, j)

            turned == False

    for i in range(0, 500, 64):
        for j in range(0, 500, 64):
            surface(i, j)

    robot(robotX, robotY)

    UpdateCurrentMovement("halt")

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
