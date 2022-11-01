import pygame
import requests
import json

pygame.init()
clock = pygame.time.Clock()
pygame.key.set_repeat(20, 20)
screensize = (500, 500)
scene = pygame.display.set_mode(screensize)
CurrentButton = "none"  # current button being pressed
robotBody = pygame.image.load("kermit.png")
robotRect = robotBody.get_rect()

groundSprite = pygame.image.load('floor.jpg')

robotX = 225
robotY = 225


def robot(x, y):
    scene.blit(robotBody, (x, y))
    robotRect.x = x
    robotRect.y = y


def robotControl(left, down, right, up):
    global robotX, robotY
    speed = 5
    if not robotX <= 0:
        robotX += speed * left
    if not robotX >= 430:
        robotX += speed * right
    if not robotY >= 430:
        robotY -= speed * down
    if not robotY <= 0:
        robotY -= speed * up


def surface(x, y):
    scene.blit(groundSprite, (x, y))


def ChangeMovementMode(mode):
    if mode == "remote":
        res = requests.get("http://192.168.1.7:8080/ChangeMoveMode/remote")
        print(res)
    elif mode == "auto":
        res = requests.get("http://192.168.1.7:8080/ChangeMoveMode/auto")
        print(res)
    elif mode == "roam":
        res = requests.get("http://192.168.1.7:8080/ChangeMoveMode/roam")
        print(res)
    elif mode == "idle":
        res = requests.get("http://192.168.1.7:8080/ChangeMoveMode/idle")
        print(res)
    else:
        print("error, mode not accepted")


def SendButtonPress(buttons):
    try:
        res = requests.get(f"http://192.168.1.7:8080/ButtonPress/{buttons}", timeout=0.01)
        print(res)
    except requests.exceptions.Timeout as err:
        pass


def UpdateCurrentButton(button):
    if button != CurrentButton:
        SendButtonPress(button)
        return button
    return button


starting = True
while starting:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            starting = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            CurrentButton = UpdateCurrentButton("a")
            if keys[pygame.K_s]:
                CurrentButton = UpdateCurrentButton("as")
                robotControl(-0.01, -0.01, 0, 0)
            if keys[pygame.K_w]:
                CurrentButton = UpdateCurrentButton("aw")
                robotControl(-0.01, 0, 0, 0.01)
            if keys[pygame.K_d]:
                CurrentButton = UpdateCurrentButton("ad")
                robotControl(0, 0, 0, 0)
            else:
                robotControl(-0.7, 0, 0, 0)
        if keys[pygame.K_s]:
            CurrentButton = UpdateCurrentButton("s")
            if keys[pygame.K_a]:
                CurrentButton = UpdateCurrentButton("as")
                robotControl(-0.01, -0.01, 0, 0)
            if keys[pygame.K_d]:
                CurrentButton = UpdateCurrentButton("sd")
                robotControl(0, -0.01, 0.01, 0)
            if keys[pygame.K_w]:
                CurrentButton = UpdateCurrentButton("sw")
                robotControl(0, 0, 0, 0)
            else:
                robotControl(0, -0.7, 0, 0)
        if keys[pygame.K_d]:
            CurrentButton = UpdateCurrentButton("d")
            if keys[pygame.K_s]:
                CurrentButton = UpdateCurrentButton("sd")
                robotControl(0, -0.01, 0.01, 0)
            if keys[pygame.K_w]:
                CurrentButton = UpdateCurrentButton("dw")
                robotControl(0, 0, 0.01, 0.01)
            if keys[pygame.K_a]:
                CurrentButton = UpdateCurrentButton("ad")
                robotControl(0, 0, 0, 0)
            else:
                robotControl(0, 0, 0.7, 0)
        if keys[pygame.K_w]:
            CurrentButton = UpdateCurrentButton("w")
            if keys[pygame.K_a]:
                CurrentButton = UpdateCurrentButton("aw")
                robotControl(-0.01, 0, 0, 0.01)
            if keys[pygame.K_d]:
                CurrentButton = UpdateCurrentButton("dw")
                robotControl(0, 0, 0.01, 0.01)
            if keys[pygame.K_s]:
                CurrentButton = UpdateCurrentButton("sw")
                robotControl(0, 0, 0, 0)
            else:
                robotControl(0, 0, 0, 0.7)
        if not keys:
            CurrentButton = UpdateCurrentButton("none")
    for i in range(0, 500, 64):
        for j in range(0, 500, 64):
            surface(i, j)

    robot(robotX, robotY)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
