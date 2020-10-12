import pygame, sys
from pygame.locals import *

pygame.init()
vec = pygame.math.Vector2

FPS = 60
#Size of display:
WIDTH = 500
HEIGHT = 500
#Colors:
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (125, 183, 255)
GRASS_GREEN = (14, 176, 19)
ORANGE = (224, 129, 13)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
frame_per_tick = pygame.time.Clock()

image = pygame.image.load("superthomas/super_thomas_sheet.png").convert_alpha()
surface = pygame.Surface((32, 32))
surface.set_colorkey(BLACK)
rect = surface.get_rect()
rect.center = vec(WIDTH/2, HEIGHT/2)
surface.blit(image, (0, 0), (0, 0, 32, 32))
surface.blit(image, (0, 0), (0, 32, 32, 32))

while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(BLUE)
    screen.blit(surface, rect)

    pygame.display.update()
    frame_per_tick.tick(FPS)