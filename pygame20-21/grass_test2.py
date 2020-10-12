import pygame
from pygame.locals import *
import sys
import random, math

pygame.init()
vec = pygame.math.Vector2

FPS = 30
#Size of display:
WIDTH = 500
HEIGHT = 500
#Colors:
WHITE = (255, 255, 255)
BLUE = (125, 183, 255)
GRASS_GREEN = (14, 176, 19)
#some constants:

GRASS_DENSITY = 3 #minimum straw distance in pixels
WIND_ANGLE = 10

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

GROUND = platform()

class Grass():
    def __init__(self):
        self.grass_sheet = pygame.image.load("Grass/grass_sheet.png").convert()
        self.grass_sheet.set_colorkey(WHITE)
        self.wind_factor = random.randint(280, 320)
        
    
    def draw(self, x_pos):
        self.grass_type = random.randint(1, 4)
        
        if self.grass_type == 1:
            self.straw = self.grass_sheet.subsurface(0, 0, 8, 25)
        elif self.grass_type == 2:
            self.straw = self.grass_sheet.subsurface(10, 0, 8, 25)
        elif self.grass_type == 3:
            self.straw = self.grass_sheet.subsurface(20, 0, 8, 25)
        else:
            self.straw = self.grass_sheet.subsurface(30, 0, 8, 25)
        self.pos = vec(x_pos, HEIGHT -45 +random.randint(0, 5))

        self.straw_width = self.straw.get_rect().width
        self.origin_x = self.pos.x
    
    def wind(self):
        self.ticks = pygame.time.get_ticks()/self.wind_factor
        self.angle = math.sin(self.ticks)*WIND_ANGLE
        self.rot_straw = pygame.transform.rotate(self.straw, self.angle)
        self.rot_straw_width = self.rot_straw.get_rect().width
        if self.angle > 0:
            self.pos.x = self.origin_x - self.rot_straw_width + self.straw_width
        else:
            self.pos.x = self.origin_x
        screen.blit(self.rot_straw, self.pos)
"""
sprite_pos1 = (WIDTH-250, HEIGHT-45)
sprite_pos2 = (WIDTH-260, HEIGHT-45)
grass_sheet = pygame.image.load("Grass/grass_sheet.png").convert()
grass_sheet.set_colorkey((255, 255, 255))

grass1 = grass_sheet.subsurface(0, 0, 8, 25)
grass2 = grass_sheet.subsurface(5, 0, 8, 25)

grass1 = grass()
grass1_pos = (WIDTH-250, HEIGHT-45)
grass2 = grass()
grass2_pos = (WIDTH-270, HEIGHT-45)
"""
grass_list = []
x = 0
pos_x = 10
while pos_x <= WIDTH-15:
    pos_x = 10 + GRASS_DENSITY*x + random.randint(0, 2)
    pos = vec(pos_x, HEIGHT - 45 + random.randint(0, 3))
    grass = Grass()
    grass.draw(pos_x)
    grass_list.append(grass)
    x += 1

while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    screen.fill(BLUE)
    
    for straw in grass_list:
        straw.wind()
    screen.blit(GROUND.surf, GROUND.rect)
    pygame.display.update()
    frame_per_tick.tick(FPS)