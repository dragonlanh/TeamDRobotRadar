import pygame

# define constants  
WIDTH = 500
HEIGHT = 500
FPS = 60

# define colors  
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# initialize pygame and create screen  
pygame.init()
wn = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Create image

img0 = pygame.image.load('./Robot.png')
img0 = pygame.transform.scale(img0, (50, 50))

img0.set_colorkey(BLACK)
rect0 = img0.get_rect()
rect0.center = (WIDTH // 2, HEIGHT // 2)


def blitRotate2(surf, image, topleft, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=topleft).center)
    surf.blit(rotated_image, new_rect.topleft)


def RotateRobot(angle):
    pygame.transform.rotate(img0, angle)


angle = 0
run = True
wn.blit(img0, rect0)
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        angle += 1
        wn.fill(BLACK)
        blitRotate2(wn, img0, rect0.topleft, angle)

    if keys[pygame.K_d]:
        angle -= 1
        wn.fill(BLACK)
        blitRotate2(wn, img0, rect0.topleft, angle)

    clock.tick(FPS)
    pygame.display.flip()

pygame.quit()
pygame.quit()
