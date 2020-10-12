import pygame, sys, random, math
from pygame.locals import *

pygame.init()
vec = pygame.math.Vector2

FPS = 60
#Size of display:
WIDTH = 500
HEIGHT = 500
#Colors:
WHITE = (255, 255, 255)
BLUE = (125, 183, 255)
GRASS_GREEN = (14, 176, 19)
ORANGE = (224, 129, 13)
RED = (212, 27, 17)
#Character constants:
PLAYER_WIDTH = 30
PLAYER_HEIGHT = 70
ACC = 0.5
FRIC = -0.12

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Player sprite")
screen.fill((BLUE))

frame_per_tick = pygame.time.Clock()

class platform(pygame.sprite.Sprite):
    def __init__(self, width, height, color, plat_center):
        super().__init__()
        self.surf = pygame.Surface((width, height))
        self.surf.fill(color)
        self.rect = self.surf.get_rect(center = plat_center)

class character(pygame.sprite.Sprite):
    def __init__(self, c_size, color, c_pos): #c_size needs to be a Vector2 object!!
        super().__init__()
        self.surf = pygame.Surface(c_size)
        self.surf.fill(color)
        self.rect = self.surf.get_rect()
        self.size = c_size
        self.pos = vec(c_pos)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
    def update(self):
        self.colliding = pygame.sprite.spritecollide(self, player_group, False)

        if self.colliding:
            self.pla_cntr = self.colliding[0].rect.left + self.colliding[0].rect.width/2
            if self.pos.x < self.pla_cntr: # player coming from the right, pushing to the left
                self.pos.x = self.colliding[0].rect.left - self.size.x/2 - 1
            elif self.pos.x > self.pla_cntr: # player coming from the left, pushing to the right
                self.pos.x = self.colliding[0].rect.left + self.colliding[0].rect.width + self.size.x/2 + 1

        if self.pos.x > WIDTH:
            self.pos.x = 1
        elif self.pos.x < 0:
            self.pos.x = WIDTH -1

        self.rect.midbottom = self.pos


class player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.surf.fill(ORANGE)
        self.rect = self.surf.get_rect()

        self.pos = vec((WIDTH/2, HEIGHT-55))
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def move(self):
        self.acc = vec(0, 0.5)
        self.pressed_keys = pygame.key.get_pressed()

        if self.pressed_keys[K_a]:
            self.acc.x = -ACC
        elif self.pressed_keys[K_d]:
            self.acc.x = ACC

        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel

        if self.pos.x > WIDTH:
            self.pos.x = 0
        elif self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.midbottom = self.pos

    def update(self):
        self.colliding = pygame.sprite.spritecollide(self, platform_group, False)
        
        if self.colliding:
            self.pos.y = self.colliding[0].rect.top + 1
            self.vel.y = 0

GROUND = platform(WIDTH, 20, GRASS_GREEN, (WIDTH/2, 490))
PLAYER1 = player()

RED_BOX = character(vec(40, 40), RED, vec(300, HEIGHT-20))
player_group = pygame.sprite.Group()
player_group.add(PLAYER1)
platform_group = pygame.sprite.Group()
platform_group.add(GROUND)

while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        
    screen.fill(BLUE)
    RED_BOX.update()
    PLAYER1.update()
    screen.blit(PLAYER1.surf, PLAYER1.rect)
    screen.blit(RED_BOX.surf, RED_BOX.rect)
    PLAYER1.move()
    screen.blit(GROUND.surf, GROUND.rect)
    pygame.display.update()
    frame_per_tick.tick(FPS)