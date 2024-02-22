import pygame
import requests
import json
import math
import Classes
import random
import time
from PIL import Image

pygame.init()
HEIGHT = 600
WIDTH = 1200
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Team D Robot Radar")
icon_img = pygame.image.load("./logo.ico")
pygame.display.set_icon(icon_img)
Current_Movement_Mode = "idle"
CurrentButton = "none"
ServerConnection = "False"
RobotStatus = "Not Connected"
ObstacleFound = False
currentMovement = "none"
turned = False
facing = "up"
turnControl = ""
speed = .45
CurrentButtonBool = "false"


# button class, probably going move to a different file
class Button:
    def __init__(self, text, width, height, position, elevation, function, mode):
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elevation = elevation
        self.originalYpos = position[1]
        self.function = function
        self.mode = mode
        # top rectangle
        self.top_rect = pygame.Rect(position, (width, height))
        self.top_color = '#ABB8C3'
        # bottom rectangle
        self.bottom_rect = pygame.Rect(position, (width, elevation))
        self.bottom_color = "#484e53"
        # text handling
        self.text_surface = pygame.font.Font(None, 30).render(text, True, '#FFFFFF')
        self.text_rect = self.text_surface.get_rect(center=self.top_rect.center)

    def draw(self):
        # button "elevation" handing
        self.top_rect.y = self.originalYpos - self.dynamic_elevation
        self.text_rect.center = self.top_rect.center
        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elevation
        # draw button on screen
        pygame.draw.rect(screen, self.bottom_color, self.bottom_rect, border_radius=12)
        pygame.draw.rect(screen, self.top_color, self.top_rect, border_radius=12)
        screen.blit(self.text_surface, self.text_rect)
        self.Check_Click()

    def Check_Click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            # basically, if hovering, change color
            self.top_color = "#5b636a"
            if pygame.mouse.get_pressed()[0]:
                # change button elevation on press
                self.dynamic_elevation = 0
                self.pressed = True
            else:
                if self.pressed == True:
                    # this is the code that runs when the button is pressed
                    self.pressed = False
                    self.dynamic_elevation = self.elevation
                    # run associated function
                    self.ClickFunc(self.mode)

        else:
            # mouse no longer hovering
            self.top_color = "#ABB8C3"
            self.dynamic_elevation = self.elevation

    def ClickFunc(self, mode):
        function = self.function(mode)
        return function


class Map:
    def __init__(self, image, pos, width, height):
        self.image = image
        self.position = pos
        self.width = width
        self.height = height
        self.Obstacles = []
        # create rectangle for map
        self.Map_img = pygame.image.load(image).convert_alpha()
        self.Map_rect = pygame.Rect(pos, (width, height))
        # self.GenerateObstacle()

    def draw(self):
        pygame.draw.rect(screen, '#484e53', self.Map_rect)
        screen.blit(self.Map_img, self.Map_rect)
        self.DrawObstacles()

    def AddObstacles(self, X, Y):
        newObstacle = Classes.Obstacle(len(self.Obstacles) + 1, X, Y)
        self.Obstacles.append(newObstacle)
        try:
            res = requests.post("http://192.168.1.8:8080/ObstacleJson", data=self.MakeObstacleJson(), timeout=1)
            print(res)
        except requests.exceptions.Timeout as err:
            print("timeout error")

    def MakeObstacleJson(self):
        compiledJson = {}
        for obstacle in self.Obstacles:
            compiledJson[obstacle.ID] = (obstacle.GetXY_Adjusted())
        print(compiledJson)
        return compiledJson

    def GenerateObstacle(self):
        for i in range(3):
            self.AddObstacles(self.Map_rect.topleft[0] + random.randint(20, 400),
                              self.Map_rect.topleft[1] + random.randint(20, 400))

    def DrawObstacles(self):
        for obstacle in self.Obstacles:
            pygame.draw.circle(screen, "PURPLE", (obstacle.GetX(), obstacle.GetY()), 6)


# functions
def SendMovement(movement):
    try:
        res = requests.get(f"http://192.168.1.8:8080/ButtonPress/{movement}", timeout=.5)
        print(res)
    except requests.exceptions.Timeout as err:
        pass


def SendButtonBool(bools):
    try:
        res = requests.get(f"http://192.168.1.8:8080/ChangeButtonBool/{bools}", timeout=0.1)
        print(res)
    except requests.exceptions.Timeout as err:
        pass


def SendButtonPress(buttons):
    try:
        res = requests.get(f"http://192.168.1.8:8080/ButtonPress/{buttons}", timeout=0.01)
        print(res)
    except requests.exceptions.Timeout as err:
        pass


def GetInfo(frameNum):
    if frameNum == 59:
        try:
            res = requests.get("http://192.168.1.8:8080/info")
            serverdata = res.content.decode()
            converted = json.loads(serverdata)
            return converted
        except requests.ConnectionError as err:
            return None


def getDistance():
    try:
        res = requests.get("http://192.168.1.8:8080/GetDistance")
        distData = res.content.decode()
        converted = json.loads(distData)
        return converted['ChangeDistance']
    except requests.exceptions.Timeout as err:
        return None


def TakePhoto(temp):
    img1 = Image.open("C:\GitHubProjects\img1.png")
    img2 = Image.open("C:\GitHubProjects\img2.png")
    img3 = Image.open("C:\GitHubProjects\img3.png")
    img4 = Image.open("C:\GitHubProjects\img4.png")
    pano = Image.new("RGB", (1000, 250), "white")
    pano.paste(img1, (0, 0))
    pano.paste(img2, (250, 0))
    pano.paste(img3, (500, 0))
    pano.paste(img4, (750, 0))
    pano.show()



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
    # turnControl = isTurned()
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
    # turnControl = isTurned()
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
    # turnControl = isTurned()
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
    # turnControl = isTurned()
    facing = "down"


def isTurned():
    try:
        res = requests.get("http://192.168.1.8:8080/GetTurn")
        data = res.content.decode()
        converted = json.loads(data)
        print(converted['ChangeTurn'])
        return converted['ChangeTurn']
    except requests.exceptions.Timeout as err:
        print("timeout error")


def ChangeMovementMode(mode):
    global Current_Movement_Mode
    if mode == "remote":
        res = requests.get("http://192.168.1.8:8080/ChangeMoveMode/remote")
        Current_Movement_Mode = "remote"
        print(res)
    elif mode == "auto":
        res = requests.get("http://192.168.1.8:8080/ChangeMoveMode/auto")
        Current_Movement_Mode = "auto"
        print(res)
    elif mode == "roam":
        res = requests.get("http://192.168.1.8:8080/ChangeMoveMode/roam")
        Current_Movement_Mode = "roam"
        print(res)
    elif mode == "idle":
        res = requests.get("http://192.168.1.8:8080/ChangeMoveMode/idle")
        Current_Movement_Mode = "idle"
    elif mode == "takephoto":
        res = requests.get("http://192.168.1.8:8080/ChangeMoveMode/takephoto")
        Current_Movement_Mode = "idle"
    else:
        print("error, mode not accepted")


def UpdateCurrentButton(button):
    if button != CurrentButton:
        SendButtonPress(button)
        return button
    return button


def UpdateButtonBool(bool):
    if bool != CurrentButtonBool:
        SendButtonBool(bool)
        return bool
    return bool


def UpdateCurrentMovement(movement):
    if movement != currentMovement:
        SendMovement(movement)
        return movement
    return movement


def MoveRobot(down, ang):
    global RobotX, RobotY
    rad = math.radians(-1 * ang)
    velocity = 2
    predicted_coords = (RobotX - down * (velocity * math.sin(rad)), RobotY + down * (velocity * math.cos(rad)))
    if not predicted_coords[0] >= RobotMap.Map_rect.topright[0] - 50:
        if not predicted_coords[0] <= RobotMap.Map_rect.topleft[0]:
            if not predicted_coords[1] >= RobotMap.Map_rect.bottomleft[1] - 50:
                if not predicted_coords[1] <= RobotMap.Map_rect.topleft[1]:
                    RobotX -= down * (velocity * math.sin(rad))
                    RobotY += down * (velocity * math.cos(rad))


def AutoMoveRobot(down, ang):
    global RobotX, RobotY
    rad = math.radians(-1 * ang)
    velocity = 2
    predicted_coords = (RobotX - down * (velocity * math.sin(rad)), RobotY + down * (velocity * math.cos(rad)))
    if not predicted_coords[0] >= RobotMap.Map_rect.topright[0] - 50:
        if not predicted_coords[0] <= RobotMap.Map_rect.topleft[0]:
            if not predicted_coords[1] >= RobotMap.Map_rect.bottomleft[1] - 50:
                if not predicted_coords[1] <= RobotMap.Map_rect.topleft[1]:
                    RobotX += down * (velocity * math.sin(rad))
                    RobotY -= down * (velocity * math.cos(rad))


def GetObstacleCoords(dist, ang):
    x = RobotX
    y = RobotY
    rad = math.radians(-1 * ang)
    predicted_coords = (RobotX - (dist * math.sin(rad)), RobotY + (dist * math.cos(rad)))
    if not predicted_coords[0] >= RobotMap.Map_rect.topright[0] - 50:
        if not predicted_coords[0] <= RobotMap.Map_rect.topleft[0]:
            if not predicted_coords[1] >= RobotMap.Map_rect.bottomleft[1] - 50:
                if not predicted_coords[1] <= RobotMap.Map_rect.topleft[1]:
                    x += (dist * math.sin(rad))
                    y -= (dist * math.cos(rad))
                    return x + 25, y + 25


def UpdateRobotRect(x, y):
    Robot_rect.x = x
    Robot_rect.y = y
    new_rect = rotated_image.get_rect(center=Robot_img.get_rect(topleft=Robot_rect.topleft).center)
    screen.blit(rotated_image, new_rect)


# load images
Robot_img = pygame.image.load("./Robot.png").convert_alpha()
Robot_rect = Robot_img.get_rect()

# create buttons
IdleButton = Button("Idle", 200, 40, (20, 40), 5, ChangeMovementMode, "idle")
RemoteButton = Button("Remote", 200, 40, (20, 90), 5, ChangeMovementMode, "remote")
AutoButton = Button("Autonomous", 200, 40, (20, 140), 5, ChangeMovementMode, "auto")
RoamButton = Button("Roam", 200, 40, (20, 190), 5, ChangeMovementMode, "roam")
PhotoButton = Button("Take Pano", 150, 40, (900, 270), 5, ChangeMovementMode, "takephoto")

# create map variable
RobotMap = Map('./Map.png', (300, 20), 500, 500)
Robot_rect.center = RobotMap.Map_rect.center
RobotX = Robot_rect.centerx
RobotY = Robot_rect.centery

font = pygame.font.Font(None, 30)
ConnText = font.render(f"Server : {ServerConnection}", True, "#000000")
ConnTextRect = ConnText.get_rect()
ConnTextRect.topleft = (20, 400)

ModeText = font.render(f"Mode : {Current_Movement_Mode}", True, "#000000")
ModeTextRect = ConnText.get_rect()
ModeTextRect.topleft = (20, 430)

RobotText = font.render(f"Robot Status : {RobotStatus}", True, "#000000")
RobotTextRect = RobotText.get_rect()
RobotTextRect.topleft = (20, 460)
# robot image
rotated_image = pygame.transform.rotate(Robot_img, 0)


def updateScreen():
    screen.fill("#DCE5ED")
    IdleButton.draw()
    RemoteButton.draw()
    AutoButton.draw()
    RoamButton.draw()
    PhotoButton.draw()
    RobotMap.draw()
    screen.blit(ConnText, ConnTextRect)
    screen.blit(ModeText, ModeTextRect)
    screen.blit(RobotText, RobotTextRect)
    # placeholder camera box
    camera = pygame.Rect(900, 20, 200, 200)
    pygame.draw.rect(screen, '#000000', camera)


def avoidObstacle():
    global currentMovement
    global frame
    global rotated_image
    global turned
    global angle
    global facing
    i = 0
    newFacing = facing

    if facing == "right":
        faceDown()
        angle = -180
        rotated_image = pygame.transform.rotate(Robot_img, angle)
        turned = True

    if facing == "left":
        faceUp()
        angle = 0
        rotated_image = pygame.transform.rotate(Robot_img, angle)
        turned = True

    if facing == "up":
        faceRight()
        angle = -90
        rotated_image = pygame.transform.rotate(Robot_img, angle)
        turned = True

    if facing == "down":
        faceLeft()
        angle = 90
        rotated_image = pygame.transform.rotate(Robot_img, angle)
        turned = True

    if isTurned() == "turned":
        while i <= 50:
            currentMovement = UpdateCurrentMovement("fwd")
            AutoMoveRobot(.3, angle)
            UpdateRobotRect(RobotX, RobotY)
            pygame.display.update()
            if frame == 59:
                frame = 0
            else:
                frame += 1
            clock.tick(60)
            pygame.display.flip()
            updateScreen()
            i += 1

    if newFacing == "right":
        faceRight()
        angle = -90
        rotated_image = pygame.transform.rotate(Robot_img, angle)
        turned = True

    if newFacing == "left":
        faceLeft()
        angle = 90
        rotated_image = pygame.transform.rotate(Robot_img, angle)
        turned = True

    if newFacing == "up":
        faceUp()
        angle = 0
        rotated_image = pygame.transform.rotate(Robot_img, angle)
        turned = True

    if newFacing == "down":
        faceDown()
        angle = -180
        rotated_image = pygame.transform.rotate(Robot_img, angle)
        turned = True


# main loop
angle = 0
running = True
frame = 0
while running:
    data = GetInfo(frame)
    # data = None
    if data is not None:
        Current_Movement_Mode = data["Mode"]
        ServerConnection = "Connected"
        RobotStatus = data["RobotStatus"]
        ConnText = font.render(f"Server : {ServerConnection}", True, "#000000")
        ModeText = font.render(f"Mode : {Current_Movement_Mode}", True, "#000000")
        RobotText = font.render(f"Robot Status : {RobotStatus}", True, "#000000")
        if data["ObstacleFound"] == False:
            ObstacleFound = False
        else:
            ObstacleFound = True
            distance = getDistance()
            convdist = int(distance)
            coords = GetObstacleCoords(convdist, angle)
            RobotMap.AddObstacles(coords[0], coords[1])
    else:
        ServerConnection = "Connection Error"

    # update screen
    screen.fill("#DCE5ED")
    IdleButton.draw()
    RemoteButton.draw()
    AutoButton.draw()
    RoamButton.draw()
    PhotoButton.draw()
    RobotMap.draw()
    screen.blit(ConnText, ConnTextRect)
    screen.blit(ModeText, ModeTextRect)
    screen.blit(RobotText, RobotTextRect)
    # placeholder camera box
    camera = pygame.Rect(900, 20, 200, 200)
    pygame.draw.rect(screen, '#000000', camera)
    # pygame events/ key presses
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if Current_Movement_Mode == "remote":
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                angle += 1
                CurrentButtonBool = UpdateButtonBool("true")
                CurrentButton = UpdateCurrentButton("a")
                rotated_image = pygame.transform.rotate(Robot_img, angle)

            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                CurrentButtonBool = UpdateButtonBool("true")
                CurrentButton = UpdateCurrentButton("s")
                MoveRobot(1, angle)

            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                angle -= 1
                CurrentButtonBool = UpdateButtonBool("true")
                CurrentButton = UpdateCurrentButton("d")
                rotated_image = pygame.transform.rotate(Robot_img, angle)

            if keys[pygame.K_w] or keys[pygame.K_UP]:
                CurrentButtonBool = UpdateButtonBool("true")
                CurrentButton = UpdateCurrentButton("w")
                if ObstacleFound == False:
                    MoveRobot(-1, angle)
                else:
                    intDistance = getDistance()
                    convIntDistance = int(intDistance)
                    print(convIntDistance)
                    if convIntDistance > 30:
                        MoveRobot(-1, angle)
            else:
                CurrentButtonBool = UpdateButtonBool("false")
            print(angle)

        if Current_Movement_Mode == "auto":

            intDistance = int(getDistance())
            currentMovement = UpdateCurrentMovement("halt")

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                print(pos)

                if not pos[0] >= RobotMap.Map_rect.topright[0] - 50:
                    if not pos[0] <= RobotMap.Map_rect.topleft[0]:
                        if not pos[1] >= RobotMap.Map_rect.bottomleft[1] - 50:
                            if not pos[1] <= RobotMap.Map_rect.topleft[1]:
                                turnedRight = False
                                turnedUp = False

                                # right
                                while pos[0] > RobotX:
                                    if facing != "right" and turned == False:
                                        faceRight()
                                        angle = -90
                                        rotated_image = pygame.transform.rotate(Robot_img, angle)
                                        turned = True
                                    if isTurned() == "turned":
                                        while pos[0] > RobotX:
                                            currentMovement = UpdateCurrentMovement("fwd")
                                            AutoMoveRobot(.3, angle)
                                            UpdateRobotRect(RobotX, RobotY)
                                            pygame.display.update()
                                            if frame == 59:
                                                frame = 0
                                            else:
                                                frame += 1
                                            clock.tick(60)
                                            pygame.display.flip()
                                            updateScreen()
                                            intDistance = int(getDistance())
                                            if data["ObstacleFound"] == True:
                                                intDistance = getDistance()
                                                convIntDistance = int(intDistance)
                                                print(convIntDistance)
                                                if convIntDistance <= 30:
                                                    avoidObstacle()
                                    turnedRight = True

                                turned = False

                                # left
                                if turnedRight == False:
                                    while pos[0] < RobotX:
                                        if facing != "left" and turned == False:
                                            faceLeft()
                                            angle = 90
                                            rotated_image = pygame.transform.rotate(Robot_img, angle)
                                            turned = True
                                        if isTurned() == "turned":
                                            while pos[0] < RobotX:
                                                currentMovement = UpdateCurrentMovement("fwd")
                                                AutoMoveRobot(.3, angle)
                                                UpdateRobotRect(RobotX, RobotY)
                                                pygame.display.update()
                                                if frame == 59:
                                                    frame = 0
                                                else:
                                                    frame += 1
                                                clock.tick(60)
                                                pygame.display.flip()
                                                updateScreen()
                                                intDistance = int(getDistance())
                                                if data["ObstacleFound"] == True:
                                                    intDistance = getDistance()
                                                    convIntDistance = int(intDistance)
                                                    print(convIntDistance)
                                                    if convIntDistance <= 30:
                                                        avoidObstacle()

                                turned = False

                                # up
                                while pos[1] < RobotY:
                                    if facing != "up" and turned == False:
                                        faceUp()
                                        # while turnControl != "turned":
                                        #   turnControl = isTurned()
                                        angle = 0
                                        rotated_image = pygame.transform.rotate(Robot_img, angle)
                                        turned = True
                                    if isTurned() == "turned":
                                        while pos[1] < RobotY:
                                            currentMovement = UpdateCurrentMovement("fwd")
                                            AutoMoveRobot(.3, angle)
                                            UpdateRobotRect(RobotX, RobotY)
                                            pygame.display.update()
                                            if frame == 59:
                                                frame = 0
                                            else:
                                                frame += 1
                                            clock.tick(60)
                                            pygame.display.flip()
                                            updateScreen()
                                            intDistance = int(getDistance())
                                            if data["ObstacleFound"] == True:
                                                intDistance = getDistance()
                                                convIntDistance = int(intDistance)
                                                print(convIntDistance)
                                                if convIntDistance <= 30:
                                                    avoidObstacle()
                                    turnedUp = True

                                turned = False

                                # down
                                if turnedUp == False:
                                    while pos[1] > RobotY:
                                        if facing != "down" and turned == False:
                                            faceDown()
                                            #  while turnControl != "turned":
                                            #     turnControl = isTurned()
                                            angle = 180
                                            rotated_image = pygame.transform.rotate(Robot_img, angle)
                                            turned = True
                                        if isTurned() == "turned":
                                            while pos[1] > RobotY:
                                                currentMovement = UpdateCurrentMovement("fwd")
                                                AutoMoveRobot(.3, angle)
                                                UpdateRobotRect(RobotX, RobotY)
                                                pygame.display.update()
                                                if frame == 59:
                                                    frame = 0
                                                else:
                                                    frame += 1
                                                clock.tick(60)
                                                pygame.display.flip()
                                                updateScreen()
                                                intDistance = int(getDistance())
                                                if data["ObstacleFound"] == True:
                                                    intDistance = getDistance()
                                                    convIntDistance = int(intDistance)
                                                    print(convIntDistance)
                                                    if convIntDistance <= 30:
                                                        avoidObstacle()

                                turned = False
                            currentMovement = UpdateCurrentMovement("halt")

    UpdateRobotRect(RobotX, RobotY)
    pygame.display.update()
    if frame == 59:
        frame = 0
    else:
        frame += 1
    clock.tick(60)
    pygame.display.flip()

pygame.quit()
