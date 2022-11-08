import pygame
import requests
import threading
import json
import math
import Classes
import random

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
        self.GenerateObstacle()

    def draw(self):
        pygame.draw.rect(screen, '#484e53', self.Map_rect)
        screen.blit(self.Map_img, self.Map_rect)
        self.DrawObstacles()

    def AddObstacles(self, X, Y):
        newObstacle = Classes.Obstacle(X, Y)
        self.Obstacles.append(newObstacle)

    def GenerateObstacle(self):
        for i in range(5):
            randomLoc = (self.Map_rect.topleft[0] + random.randint(20, 400), self.Map_rect.topleft[1] + random.randint(20, 400))
            newObstacle = Classes.Obstacle(randomLoc[0], randomLoc[1])
            self.Obstacles.append(newObstacle)

    def DrawObstacles(self):
        for obstacle in self.Obstacles:
            pygame.draw.circle(screen, "PURPLE", (obstacle.GetX(), obstacle.GetY()), 6)



# functions
def ChangeMovementMode(mode):
    global Current_Movement_Mode
    if mode == "remote":
        res = requests.get("http://129.3.216.119:8080/ChangeMoveMode/remote")
        Current_Movement_Mode = "remote"
        print(res)
    elif mode == "auto":
        res = requests.get("http://129.3.216.119:8080/ChangeMoveMode/auto")
        Current_Movement_Mode = "auto"
        print(res)
    elif mode == "roam":
        res = requests.get("http://129.3.216.119:8080/ChangeMoveMode/roam")
        Current_Movement_Mode = "roam"
        print(res)
    elif mode == "idle":
        res = requests.get("http://129.3.216.119:8080/ChangeMoveMode/idle")
        Current_Movement_Mode = "idle"
    else:
        print("error, mode not accepted")


def SendButtonPress(buttons):
    try:
        res = requests.get(f"http://129.3.216.119:8080/ButtonPress/{buttons}", timeout=0.01)
        print(res)
    except requests.exceptions.Timeout as err:
        pass


def UpdateCurrentButton(button):
    if button != CurrentButton:
        SendButtonPress(button)
        return button
    return button


def MoveRobot(down, ang):
    global RobotX, RobotY
    rad = math.radians(-1 * ang)
    velocity = 2
    if not RobotX >= RobotMap.Map_rect.topright[0] - 50 or RobotX <= RobotMap.Map_rect.topleft[0]:
        RobotX -= down * (velocity * math.sin(rad))
    if not RobotY >= RobotMap.Map_rect.bottomleft[1] - 50 or RobotY <= RobotMap.Map_rect.topleft[1]:
        RobotY += down * (velocity * math.cos(rad))


def RotateRobot(left, down, right, up):
    pygame.transform.rotate(Robot_img, 90)


def UpdateRobotRect(x, y):
    Robot_rect.x = x
    Robot_rect.y = y
    new_rect = rotated_image.get_rect(center=Robot_img.get_rect(topleft=Robot_rect.topleft).center)
    screen.blit(rotated_image, new_rect)


# not in use \/
def blitRotate2(surf, image, topleft, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=topleft).center)
    surf.blit(rotated_image, new_rect.topleft)


# load images
Robot_img = pygame.image.load("./Robot.png").convert_alpha()
Robot_rect = Robot_img.get_rect()

# create buttons
IdleButton = Button("Idle", 200, 40, (20, 40), 5, ChangeMovementMode, "idle")
RemoteButton = Button("Remote", 200, 40, (20, 90), 5, ChangeMovementMode, "remote")
AutoButton = Button("Autonomous", 200, 40, (20, 140), 5, ChangeMovementMode, "auto")
RoamButton = Button("Roam", 200, 40, (20, 190), 5, ChangeMovementMode, "roam")

# create map variable
RobotMap = Map('./Map.png', (300, 20), 500, 500)
Robot_rect.center = RobotMap.Map_rect.center
RobotX = Robot_rect.centerx
RobotY = Robot_rect.centery

# adding text
ConnText = pygame.font.Font(None, 30).render("Robot : Connected", True, "#000000")
ConnTextRect = ConnText.get_rect()
ConnTextRect.topleft = (20, 400)
rotated_image = pygame.transform.rotate(Robot_img, 0)
# main loop
angle = 0
running = True
while running:
    # update screen
    screen.fill("#DCE5ED")
    IdleButton.draw()
    RemoteButton.draw()
    AutoButton.draw()
    RoamButton.draw()
    RobotMap.draw()
    screen.blit(ConnText, ConnTextRect)
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
                CurrentButton = UpdateCurrentButton("a")
                rotated_image = pygame.transform.rotate(Robot_img, angle)

            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                CurrentButton = UpdateCurrentButton("s")
                MoveRobot(1, angle)

            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                angle -= 1
                CurrentButton = UpdateCurrentButton("d")
                rotated_image = pygame.transform.rotate(Robot_img, angle)

            if keys[pygame.K_w] or keys[pygame.K_UP]:
                CurrentButton = UpdateCurrentButton("w")
                MoveRobot(-1, angle)

    UpdateRobotRect(RobotX, RobotY)
    pygame.display.update()
    clock.tick(60)
    pygame.display.flip()

pygame.quit()
