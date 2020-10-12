import pygame
from pygame.locals import *
import sys
import random, math

pygame.init()
vec = pygame.math.Vector2

FPS = 60
WIDTH = 500
HEIGHT = 500
WHITE = (255, 255, 255)
BLUE = (125, 183, 255)
GRASS_GREEN = (14, 176, 19)
ORANGE = (224, 129, 13)

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

class Grass():
    def __init__(self):
        self.pos = vec(WIDTH/2, HEIGHT-45)
        self.origin_x = self.pos.x
        self.straw = pygame.image.load("Grass/grass1.png")
        self.straw.set_colorkey(WHITE)
        self.straw_width = self.straw.get_rect().width

    def wind(self):
        self.ticks = pygame.time.get_ticks()/300
        self.angle = math.sin(self.ticks)*15
        self.rot_straw = pygame.transform.rotate(self.straw, self.angle)
        self.rot_straw_width = self.rot_straw.get_rect().width
        if self.angle > 0:
            self.pos.x = self.origin_x - self.rot_straw_width + self.straw_width
        else:
            self.pos.x = self.origin_x
        screen.blit(self.rot_straw, self.pos)

GROUND = platform()
grass_straw1 = Grass()


while True:
    screen.fill(BLUE)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    grass_straw1.wind()
    screen.blit(GROUND.surf, GROUND.rect)
    pygame.display.update()
    frame_per_tick.tick(FPS)