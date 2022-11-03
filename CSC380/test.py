import pygame

# define constants  
WIDTH = 500  
HEIGHT = 500  
FPS = 60

# define colors  
BLACK = (0 , 0 , 0)  
GREEN = (0 , 255 , 0)  

# initialize pygame and create screen  
pygame.init()  
wn = pygame.display.set_mode((WIDTH , HEIGHT))  
clock = pygame.time.Clock()  
        
# Create image

img0 = pygame.image.load('./RobotRadar/Robot.png')
img0 = pygame.transform.scale(img0, (50,50))

img0.set_colorkey(BLACK)
rect0 = img0.get_rect()
rect0.center = (WIDTH // 2 , HEIGHT // 2)

 
def RotateRobot(angle):
    pygame.transform.rotate(img0, angle)
angle = 0
run = True
while run:  
   for event in pygame.event.get():  
      if event.type == pygame.QUIT:  
         run = False
   keys = pygame.key.get_pressed()
   if keys[pygame.K_a] :     
      angle += 1
      img1 = pygame.transform.rotate(img0 , angle) 
      rect1 = img0.get_rect()
      rect1.center = rect0.center
    
      wn.fill(BLACK)
      wn.blit(img1,rect1)
    
   clock.tick(FPS)
   pygame.display.flip()


pygame.quit()
pygame.quit()