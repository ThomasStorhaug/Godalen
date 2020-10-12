import pygame, sys, random, math
from pygame.locals import *

pygame.init()
vec = pygame.math.Vector2
c = pygame.Color
FPS = 60
#Size of screen:
WIDTH = 500
HEIGHT = 500
boom_circle = 1
#Colors:
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (125, 183, 255)
NIGHT_BLUE = (2, 0, 92)
GRASS_GREEN = (14, 176, 19)
ORANGE = (224, 129, 13)
RED = (212, 27, 17)
LASER_SHADOW = c(150, 10, 0, 120) #mulig man må konvertere surface for at alfa verdien skal funke
LASER_RED = (252, 19, 3)
LASER_CORE = (255, 169, 163)

BOX_POS_C = vec(WIDTH/2, HEIGHT-11)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
frame_per_tick = pygame.time.Clock()

las_surf = pygame.Surface((WIDTH, HEIGHT))
las_rect = las_surf.get_rect()
las_surf.set_colorkey(BLACK)
box_surf = pygame.Surface((21, 21))
box_surf.fill(ORANGE)

box_rect = box_surf.get_rect()
box_rect.center = BOX_POS_C

def laser(start, end):
    pygame.draw.line(las_surf, LASER_SHADOW, start, end, 16)
    pygame.draw.line(las_surf, LASER_RED, start, end, 8)
    pygame.draw.line(las_surf, LASER_CORE, start, end, 4)
    las_surf.convert_alpha()

def impact(pos, size):
    pygame.draw.circle(las_surf, LASER_CORE, pos, 20 + size, 20 - size)

def shootin_laser():
    pressed = pygame.mouse.get_pressed()
    pos = pygame.mouse.get_pos()
    #print(pos[0])
    las_surf.fill((0, 0, 0, 0))
    
    mouse_x, mouse_y = pos
    box_x = WIDTH/2
    box_y = HEIGHT -11
    if mouse_x == box_x:
        theta = 90
    elif mouse_x > box_x:
        theta = math.degrees(math.atan((box_y-mouse_y)/abs(mouse_x-box_x)))
    else:
        theta = 180 - math.atan((box_y-mouse_y)/abs(mouse_x-box_x))*180/math.pi
    theta_0 = math.atan(2*HEIGHT/WIDTH)*180/math.pi
    if theta < theta_0:
        end_y = box_y - abs(math.tan(math.radians(theta)))*WIDTH/2 + 1
        end_x = WIDTH - 1
    elif theta_0 <= theta < 90:
        end_y = 1
        end_x = HEIGHT/math.tan(math.radians(theta)) + box_x - 1
    elif 90 <= theta < 180 - theta_0:
        end_y = 1
        end_x = box_x - box_y/math.tan(math.radians(180 - theta)) + 1
    else:
        end_y = box_y - math.tan(math.radians(180 - theta))*box_x + 1
        end_x = 1 

    if pressed[0]:
        impact((int(end_x), int(end_y)), boom_circle)
        laser(BOX_POS_C, (end_x, end_y))


while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    if boom_circle == 20:
        boom_circle = 0
    boom_circle += 1

    shootin_laser()
    screen.fill(NIGHT_BLUE)
    screen.blit(las_surf, las_rect)
    screen.blit(box_surf, box_rect)

    pygame.display.update()
    frame_per_tick.tick(FPS)