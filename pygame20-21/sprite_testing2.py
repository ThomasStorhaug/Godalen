import pygame, sys, random, math
from pygame.locals import *

pygame.init()
vec = pygame.math.Vector2

FPS = 60
#Size of screen:
WIDTH = 500
HEIGHT = 500

#Size of window:
#W_WIDTH = 1000
#W_HEIGHT = 1000

#Colors:
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (125, 183, 255)
NIGHT_BLUE = (2, 0, 92)
GRASS_GREEN = (14, 176, 19)
ORANGE = (224, 129, 13)
RED = (212, 27, 17)
#Character constants:
idle_sprites = [
    (0, 0, 32, 32),
    (32, 0, 32, 32),
    (64, 0, 32, 32),
    (96, 0, 32, 32)
]
idle_cape_sprites = [
    (0, 32, 32, 32),
    (32, 32, 32, 32),
    (64, 32, 32, 32),
    (96, 32, 32, 32)
]
running_sprites = [
    (128, 0, 32, 32),
    (160, 0, 32, 32),
    (192, 0, 32, 32),
    (224, 0, 32, 32),
    (256, 0, 32, 32),
    (288, 0, 32, 32),
    (320, 0, 32, 32),
    (352, 0, 32, 32)
]
running_cape_sprites = [
    (128, 32, 32, 32),
    (160, 32, 32, 32),
    (192, 32, 32, 32),
    (224, 32, 32, 32),
    (256, 32, 32, 32),
    (288, 32, 32, 32),
    (320, 32, 32, 32),
    (352, 32, 32, 32)
]
cape_sprite = (384, 32, 32, 32)
ACC = 0.5
FRIC = -0.12
START_POSITION = vec(WIDTH/2, 425)
# --== some functions ==--

def blit_sprite(sheet_name, type, index, surface):
    file_name = "".join(("superthomas/", sheet_name, ".png"))
    sheet = pygame.image.load(file_name).convert()
    if type == "idle":
        surface.blit(sheet, (0, 0), idle_sprites[index])
    elif type == "running":
        surface.blit(sheet, (0, 0), running_sprites[index])
    surface.set_colorkey(BLACK)

def blit_cloak(sheet_name, type, index, surface):
    file_name = "".join(("superthomas/", sheet_name, ".png"))
    sheet = pygame.image.load(file_name).convert_alpha()
    if type == "idle cape":
        surface.blit(sheet, (0, 0), idle_cape_sprites[index])
    elif type == "running cape":
        surface.blit(sheet, (0, 0), running_cape_sprites[index])
    surface.set_colorkey(BLACK)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
#window = pygame.display.set_mode((W_WIDTH, W_HEIGHT))
pygame.display.set_caption("Player sprite")


frame_per_tick = pygame.time.Clock()
class player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((32, 32))
        self.rect = self.surf.get_rect()
        # må blitte i update metoden
        self.pos = vec((WIDTH/2, HEIGHT-55))
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.facing = "right"
        self.cape_on = False
        self.pickup_counter = 0

    def move(self, sprite_no):
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
        
        if self.pressed_keys[K_a]:
            blit_sprite("super_thomas_sheet", "running", sprite_no, self.surf)
            self.facing = "left"
            if self.cape_on:
                blit_cloak("super_thomas_sheet", "running cape", sprite_no, self.surf)
            self.surf = pygame.transform.flip(self.surf, True, False)
        elif self.pressed_keys[K_d]:
            blit_sprite("super_thomas_sheet", "running", sprite_no, self.surf)
            self.facing = "right"
            if self.cape_on:
                blit_cloak("super_thomas_sheet", "running cape", sprite_no, self.surf)

    def update(self, sprite_no):
        self.colliding = pygame.sprite.spritecollide(self, platform_group, False)
        self.pickup = pygame.sprite.spritecollide(self, cape_list, False)
        if cape1 in self.pickup:
            if self.pickup_counter >= 10:
                self.cape_on = True
            self.pickup_counter += 1
        if self.colliding:
            self.pos.y = self.colliding[0].rect.top + 1
            self.vel.y = 0
        if self.facing == "right":
            blit_sprite("super_thomas_sheet", "idle", sprite_no, self.surf)
            if self.cape_on:
                blit_cloak("super_thomas_sheet", "idle cape", sprite_no, self.surf)
        elif self.facing == "left":
            blit_sprite("super_thomas_sheet", "idle", sprite_no, self.surf)
            if self.cape_on:
                blit_cloak("super_thomas_sheet", "idle cape", sprite_no, self.surf)
            self.surf = pygame.transform.flip(self.surf, True, False)

        
            
class cape(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((32, 32))
        self.rect = self.surf.get_rect()
        self.pos = vec(400, 480)
        self.exists = True
        self.exists_counter = 0
        self.image = pygame.image.load("superthomas/super_thomas_sheet.png")
        

        self.surf.blit(self.image, (0, 0), cape_sprite)
        self.surf.set_colorkey(BLACK)

    def update(self):
        self.colliding = pygame.sprite.spritecollide(self, all_sprites, False)
        if player1 in self.colliding:
            if self.exists_counter >= 10:
                self.exists = False
            self.exists_counter += 1

        self.rect.midbottom = self.pos


class platform(pygame.sprite.Sprite):
    def __init__(self, width, height, color, plat_center):
        super().__init__()
        self.surf = pygame.Surface((width, height))
        self.surf.fill(color)
        self.rect = self.surf.get_rect(center = plat_center)

GROUND = platform(WIDTH, 20, GRASS_GREEN, (WIDTH/2, 490))
platform_group = pygame.sprite.Group()
platform_group.add(GROUND)

player1 = player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player1)

cape1 = cape()
cape_list = pygame.sprite.Group()
cape_list.add(cape1)

IDLE_UPDATE = pygame.USEREVENT
RUNNING_UPDATE = pygame.USEREVENT +1
pygame.time.set_timer(IDLE_UPDATE, 250)
pygame.time.set_timer(RUNNING_UPDATE, 100)
idle_index = 0
running_index = 0


while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == IDLE_UPDATE:
            if idle_index == 3:
                idle_index = 0
            else:
                idle_index += 1
        elif event.type == RUNNING_UPDATE:
            if running_index == 7:
                running_index = 0
            else:
                running_index += 1
    screen.fill(NIGHT_BLUE)
    player1.update(idle_index)
    player1.move(running_index)
    if cape1.exists:
        cape1.update()
        screen.blit(cape1.surf, cape1.rect)
    elif cape1 in cape_list:
        cape_list.remove(cape1)
    screen.blit(player1.surf, player1.rect)
    screen.blit(GROUND.surf, GROUND.rect)

    #pygame.transform.scale(screen, (W_WIDTH, W_HEIGHT), window)
    pygame.display.update()
    frame_per_tick.tick(FPS)