import json

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
turnControl = ""
speed = .45

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

def faceRight():
    global facing
    global currentMovement
    global turnControl
    if facing == "up":
        currentMovement = UpdateCurrentMovement("right")
    elif facing == "left":
        currentMovement = UpdateCurrentMovement("180")
    elif facing == "down":
        currentMovement = UpdateCurrentMovement("left")
    #turnControl = isTurned()
    facing = "right"

def faceUp():
    global facing
    global currentMovement
    global turnControl
    if facing == "right":
        currentMovement = UpdateCurrentMovement("left")
    elif facing == "left":
        currentMovement = UpdateCurrentMovement("right")
    elif facing == "down":
        currentMovement = UpdateCurrentMovement("180")
    #turnControl = isTurned()
    facing = "up"

def faceLeft():
    global facing
    global currentMovement
    global turnControl
    if facing == "up":
        currentMovement = UpdateCurrentMovement("left")
    elif facing == "right":
        currentMovement = UpdateCurrentMovement("180")
    elif facing == "down":
        currentMovement = UpdateCurrentMovement("right")
    #turnControl = isTurned()
    facing = "left"


def faceDown():
    global facing
    global currentMovement
    global turnControl
    if facing == "up":
        currentMovement = UpdateCurrentMovement("180")
    elif facing == "left":
        currentMovement = UpdateCurrentMovement("left")
    elif facing == "right":
        currentMovement = UpdateCurrentMovement("right")
    #turnControl = isTurned()
    facing = "down"


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
        res = requests.get(f"http://192.168.1.130:8080/ButtonPress/{movement}", timeout=.5)
        print(res)
    except requests.exceptions.Timeout as err:
        pass

def UpdateCurrentMovement(movement):
    if movement != currentMovement:
        SendMovement(movement)
        return movement
    return movement

def isTurned():
    try:
        res = requests.get("http://192.168.1.130:8080/GetTurn")
        data = res.content.decode()
        converted = json.loads(data)
        print(converted['ChangeTurn'])
        return converted['ChangeTurn']
    except requests.exceptions.Timeout as err:
        print("timeout error")


starting = True
while starting:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            starting = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            print(pos)

            turnedRight = False
            turnedUp = False

            #right
            while (pos[0] - 50) > robotX:
                if facing != "right" and turned == False:
                    faceRight()
                    #while turnControl != "turned":
                     #   turnControl = isTurned()
                    turned = True
                if isTurned() == "turned":
                    while (pos[0] - 50) > robotX:
                        currentMovement = UpdateCurrentMovement("fwd")
                        robotX += speed
                        robot(robotX, robotY)
                        pygame.display.flip()
                        for i in range(0, 500, 64):
                            for j in range(0, 500, 64):
                                surface(i, j)
                turnedRight = True

            turned = False

            # left
            if turnedRight == False:
                while (pos[0] - 50) < robotX:
                    if facing != "left" and turned == False:
                        faceLeft()
                      #  while turnControl != "turned":
                       #     turnControl = isTurned()
                        turned = True
                    if isTurned() == "turned":
                        while (pos[0] - 50) < robotX:
                            currentMovement = UpdateCurrentMovement("fwd")
                            robotX -= speed
                            robot(robotX, robotY)
                            pygame.display.flip()
                            for i in range(0, 500, 64):
                                for j in range(0, 500, 64):
                                    surface(i, j)

            turned = False

            # up
            while (pos[1] - 50) < robotY:
                if facing != "up" and turned == False:
                    faceUp()
                    #while turnControl != "turned":
                     #   turnControl = isTurned()
                    turned = True
                if isTurned() == "turned":
                    while (pos[1] - 50) < robotY:
                        currentMovement = UpdateCurrentMovement("fwd")
                        robotY -= speed
                        robot(robotX, robotY)
                        pygame.display.flip()
                        for i in range(0, 500, 64):
                            for j in range(0, 500, 64):
                                surface(i, j)
                turnedUp = True

            turned = False

            # down
            if turnedUp == False:
                while (pos[1] - 50) > robotY:
                    if facing != "down" and turned == False:
                        faceDown()
                      #  while turnControl != "turned":
                       #     turnControl = isTurned()
                        turned = True
                    if isTurned() == "turned":
                        while (pos[1] - 50) > robotY:
                            currentMovement = UpdateCurrentMovement("fwd")
                            robotY += speed
                            robot(robotX, robotY)
                            pygame.display.flip()
                            for i in range(0, 500, 64):
                                for j in range(0, 500, 64):
                                    surface(i, j)

            turned = False

    for i in range(0, 500, 64):
        for j in range(0, 500, 64):
            surface(i, j)

    robot(robotX, robotY)

    currentMovement = UpdateCurrentMovement("halt")

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
