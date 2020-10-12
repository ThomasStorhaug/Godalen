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
#some constants:

GRASS_DENSITY = 3 #minimum straw distance in pixels
WIND_ANGLE = 10

#sprite constants
PLAYER_WIDTH = 30
PLAYER_HEIGHT = 70
ACC = 0.5
FRIC = -0.12

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
        self.colliding = pygame.sprite.spritecollide(self, platforms, False)
        
        if self.colliding:
            self.pos.y = self.colliding[0].rect.top + 1
            self.vel.y = 0


class Grass(pygame.sprite.Sprite):
    def __init__(self, x_pos):
        super().__init__()
        GRASS_SHEET = pygame.image.load("Grass/grass_sheet.png").convert()

        self.image = pygame.Surface((8, 25))
        self.wind_factor = random.randint(280, 320)
        self.grass_type = random.randint(1, 4)
        
        if self.grass_type == 1:
            self.image.blit(GRASS_SHEET, (0, 0), (0, 0, 8, 25))
        elif self.grass_type == 2:
            self.image.blit(GRASS_SHEET, (0, 0), (10, 0, 8, 25))
        elif self.grass_type == 3:
            self.image.blit(GRASS_SHEET, (0, 0), (20, 0, 8, 25))
        else:
            self.image.blit(GRASS_SHEET, (0, 0), (30, 0, 8, 25))

        self.image.set_colorkey(WHITE)
        self.pos = vec(x_pos, HEIGHT -45 +random.randint(0, 5))
        self.rect = self.image.get_rect() #s tore the rect of the image as the appropriate variable (self.rect) to be recognized by for example collisions
        self.rect.topleft = self.pos # moves the rect to the position thats been determined for the sprite !!important!!
        self.straw_width = self.image.get_rect().width
        # --== getting the original dimensions of the straw rect: ==--
        self.origin_x = self.pos.x
        self.origin_y = self.pos.y 
        self.height = self.rect.height
    
    def update(self):
        self.colliding = pygame.sprite.spritecollide(self, player_group, False)
        self.pos.y = self.origin_y # !!important!! resets the y value so the grass wont end up in the ground
        if self.colliding:
            self.pla_cntr = self.colliding[0].rect.centerx
            self.str_cntr = self.pos.x + self.straw_width/2
            self.angle = 45/28 * (self.pla_cntr - self.str_cntr) #divide by 28 -> by experience this is the max distance between the centerlines of a rotated straw and the player
            self.rot_straw = pygame.transform.rotate(self.image, self.angle)
            self.rot_straw_width = self.rot_straw.get_rect().width
            if self.height - self.rot_straw.get_rect().height > 0:
                self.pos.y = self.origin_y + (self.height - self.rot_straw.get_rect().height)

            if self.angle > 0:
                self.pos.x = self.origin_x - self.rot_straw_width + self.straw_width
            else:
                self.pos.x = self.origin_x
            
        else:
            self.ticks = pygame.time.get_ticks()/self.wind_factor
            self.angle = math.sin(self.ticks)*WIND_ANGLE
            self.rot_straw = pygame.transform.rotate(self.image, self.angle)
            self.rot_straw_width = self.rot_straw.get_rect().width
            if self.angle > 0:
                self.pos.x = self.origin_x - self.rot_straw_width + self.straw_width
            else:
                self.pos.x = self.origin_x
        
        
        screen.blit(self.rot_straw, self.pos)


        

# --== instantiating the ground: ==--
GROUND = platform()
platforms = pygame.sprite.Group()
platforms.add(GROUND)
# --== initiating grass instances: ==--
grass_list = []
x = 0
pos_x = 10
while pos_x <= WIDTH-15:
    pos_x = 10 + GRASS_DENSITY*x + random.randint(0, 2)
    pos = vec(pos_x, HEIGHT - 45) #  + random.randint(0, 3)
    grass = Grass(pos_x)
    #grass.draw(pos_x)
    grass_list.append(grass)
    x += 1
# --==initiating the player instance: ==--
player1 = player()
player_group = pygame.sprite.Group()
player_group.add(player1)

while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    screen.fill(BLUE)
    #--== updating states of entities and drawing entities on the screen: ==--
    player1.update()
    player1.move()
    screen.blit(player1.surf, player1.rect)
    for straw in grass_list:
        straw.update() # this blits the grass straws to the screen surface aswell as move them around
    screen.blit(GROUND.surf, GROUND.rect)
    pygame.display.update()
    frame_per_tick.tick(FPS)