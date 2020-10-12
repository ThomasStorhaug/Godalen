import pygame
from pygame.locals import *
import sys
import random

pygame.init()
vec = pygame.math.Vector2

FPS = 30
WIDTH = 500
HEIGHT = 500
BLUE = (125, 183, 255)
GRASS_GREEN = (14, 176, 19)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Grass in the wind")
screen.fill((BLUE))

frame_per_tick = pygame.time.Clock()

class platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((WIDTH, 20))
        self.surf.fill(GRASS_GREEN)
        self.rect = self.surf.get_rect(center = (WIDTH/2, 490))

class grass():
    def __init__(self):
        self.surf = pygame.Surface((20, 20))
        self.wind_counter = 0
        self.right_direction = True #True for going right, False for going left

    def draw(self):
        self.start_x = random.randint(20, 480)
        self.start_coord = vec(self.start_x, 480)
        self.end_coord = vec(self.start_x, 460)
        pygame.draw.line(screen, GRASS_GREEN, self.start_coord, self.end_coord, 2)

    def wind(self):
        if self.right_direction:
            if self.wind_counter < 5:
                self.end_coord.x += 1
                self.wind_counter += 1
            else:
                self.end_coord.x -= 1
                self.wind_counter -= 1
                self.right_direction = False
        else:
            if self.wind_counter > -5:
                self.end_coord.x -= 1
                self.wind_counter -= 1
            else:
                self.end_coord.x += 1
                self.wind_counter += 1
                self.right_direction = True
        pygame.draw.line(screen, GRASS_GREEN, self.start_coord, self.end_coord, 2)



GROUND = platform()
#grass_straws = pygame.sprite.Group()

#grass_straws.add(grass1)

grass_list = []
for i in range(0, 50):
    grass_list.append(grass())
    grass_list[i].draw()

while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    screen.fill(BLUE)
    for grass in grass_list:
        grass.wind()
    screen.blit(GROUND.surf, GROUND.rect)
    pygame.display.update()
    frame_per_tick.tick(FPS)