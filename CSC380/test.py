
from tkinter import *
import pygame


root = Tk()
root.title("Team C's RoborRadar" )
root.iconbitmap(r'.\logo.ico')

def start():
   pygame.init()
   clock = pygame.time.Clock()
   pygame.key.set_repeat(20, 20)
   screensize = (500,500)
   scene = pygame.display.set_mode(screensize)

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
      global robotX,robotY
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
            starting =False
         keys = pygame.key.get_pressed()
         if keys[pygame.K_a]:
            if keys[pygame.K_s]:
               robotControl(-0.01, -0.01, 0, 0)
            if keys[pygame.K_w]:
               robotControl(-0.01, 0, 0, 0.01)
            if keys[pygame.K_d]:
               robotControl(0, 0, 0, 0)
            else:
               robotControl(-0.7, 0, 0, 0)
         if keys[pygame.K_s]:
            if keys[pygame.K_a]:
               robotControl(-0.01, -0.01, 0, 0)
            if keys[pygame.K_d]:
               robotControl(0, -0.01, 0.01, 0)
            if keys[pygame.K_w]:
               robotControl(0, 0, 0, 0)
            else:
               robotControl(0, -0.7, 0, 0)
         if keys[pygame.K_d]:
            if keys[pygame.K_s]:
               robotControl(0, -0.01, 0.01, 0)
            if keys[pygame.K_w]:
               robotControl(0, 0, 0.01, 0.01)
            if keys[pygame.K_a]:
               robotControl(0, 0, 0, 0)
            else:
               robotControl(0, 0, 0.7, 0)
         if keys[pygame.K_w]:
            if keys[pygame.K_a]:
               robotControl(-0.01, 0, 0, 0.01)
            if keys[pygame.K_d]:
               robotControl(0, 0, 0.01, 0.01)
            if keys[pygame.K_s]:
               robotControl(0, 0, 0, 0)
            else:
               robotControl(0, 0, 0, 0.7)  

      for i in range(0, 500, 64):
         for j in range(0, 500, 64):
            surface(i, j)
      
      robot(robotX, robotY)

      pygame.display.flip()
      clock.tick(60)

   pygame.quit()

startButton = Button(root, text= "Start",command = start, padx=50, pady=10 )
startButton.pack(padx=100, pady=0)



quitButton = Button(root, text='Exit Program',command=root.quit,padx=50, pady=10 )
quitButton.pack(padx=100, pady=0)

root.mainloop()