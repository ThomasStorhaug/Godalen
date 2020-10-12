import pygame, sys, random, math
from pygame.locals import *

pygame.init()
vec = pygame.math.Vector2

# ---------------------------------------------- Player constants ---------------------------------------------------------------------
#
#
GRAVITY = 0.5
ACC = 0.5
MAX_SPEED = 7

# ------------------------------------------------- Colors ----------------------------------------------------------------------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (125, 183, 255)
NIGHT_BLUE = (2, 0, 92)
GRASS_GREEN = (14, 176, 19)
ORANGE = (224, 129, 13)
RED = (212, 27, 17)
LASER_SHADOW = (150, 10, 0)
LASER_RED = (252, 19, 3)
LASER_CORE = (255, 169, 163)
# ------------------------------------------------ Main display -----------------------------------------------------------------------
WIDTH = 500
HEIGHT = 500
FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
frame_per_tick = pygame.time.Clock()
# ------------------------------------------------ Effects surface --------------------------------------------------------------------
#
#  Used for rendering effects (beams, particles etc.) - same size as the main display
EFFECTS_SURFACE = pygame.Surface((WIDTH, HEIGHT))
EFFECTS_SURFACE.set_colorkey(BLACK)
EF_RECT = EFFECTS_SURFACE.get_rect()
#------------------------------------------------ particle generation -----------------------------------------------------------------
#
# particle = [position, velocity, size]
particles = []

def particle_gen(surf, color, pos=None):
    if pos:
        particles.append([pos, [random.randint(0, 10)/10 - 1, -2], random.randint(4, 6)])

    for part in particles:
        if part[2] <= 1:
            particles.remove(part)
        else:
            part[0][0] += part[1][0]
            part[0][1] += part[1][1]
            part[1][1] += 0.2
            part[2] -= 0.1

            pygame.draw.circle(surf, color, (int(part[0][0]), int(part[0][1])), int(part[2]))
# -------------------------------------------------- tile system ----------------------------------------------------------------------
#
# each tile represented by a string: "x_coord;y_coord" - where each tile represents an area of 20 by 20 pixels
# tilestrings are keys for transformed rects(coordinates are in tile-scale, needs to be mult. by 20 to get display scale) in a dictionary
# tile: [tile_x, tile_y, color]

tile_map = {}

TILE_SIZE = 20

tile_map["10;10"] = [10, 10, ORANGE]
tile_map["11;10"] = [11, 10, ORANGE]
tile_map["12;10"] = [12, 10, ORANGE]
tile_map["13;10"] = [13, 10, ORANGE]

for i in range(25):
    tile_map[str(i) + ";24"] = [i, 24, GRASS_GREEN]

tile_map["20;23"] = [20, 23, ORANGE]

def platform():
    for tile in tile_map:
        pygame.draw.rect(screen, tile_map[tile][2], (tile_map[tile][0]*TILE_SIZE, tile_map[tile][1]*TILE_SIZE, TILE_SIZE, TILE_SIZE))

tile_list = []

for key in tile_map:
    tile_list.append(pygame.Rect(tile_map[key][0]*TILE_SIZE, tile_map[key][1]*TILE_SIZE, TILE_SIZE, TILE_SIZE))

# --------------------------------------------------- Physics --------------------------------------------------------------------------

def collision_test(rect, tiles):
    collisions = []
    for tile in tiles:
        if rect.colliderect(tile):
            collisions.append(tile)
    return collisions

def move(rect, vel, player= False): #for modularity add a tiles argument to not have to iterate through ALL tiles
    # --== move x ==--
    rect.x += vel.x
    # --== collision test == --
    collision_dict = {"right": False, "left": False, "top": False, "bottom": False}
    collisions = collision_test(rect, tile_list)
    for tile in collisions:
        if vel.x > 0:
            rect.right = tile.left
            collision_dict["right"] = True
        elif vel.x < 0:
            rect.left = tile.right
            collision_dict["left"] = True
    if rect.right > WIDTH:
        rect.left = 0
    elif rect.left < 0:
        rect.right = WIDTH
    # --== move y ==--
    rect.y += vel.y
    # --== collision test ==--
    collisions = collision_test(rect, tile_list)
    for tile in collisions:
        if vel.y < 0:
            rect.top = tile.bottom
            collision_dict["top"] = True
        elif vel.y > 0:
            rect.bottom = tile.top
            collision_dict["bottom"] = True
    return rect, collision_dict

# ---------------------------------------------------- Player --------------------------------------------------------------------------


class Player():
    def __init__(self):
        self.surf = pygame.Surface((20, 20))
        self.rect = self.surf.get_rect()
        self.surf.fill(RED)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.pos = vec(250, 450)
        self.collisions = {}
        self.rect.center = self.pos
        self.moving_right = False
        self.moving_left = False
        self.drifting = False
        self.air_timer = 0
   
    def update(self):
        #print(self.vel)
        # --== move x ==--
        self.acc = vec(0, GRAVITY)
        self.pressed_keys = pygame.key.get_pressed()

        if self.pressed_keys[K_a]:
            if abs(self.vel.x) < MAX_SPEED:
                self.acc.x = -ACC
            self.moving_right = False
            self.moving_left = True
            self.drifting = False
        elif self.pressed_keys[K_d]:
            if abs(self.vel.x) < MAX_SPEED:
                self.acc.x = ACC
            self.moving_left = False
            self.moving_right = True
            self.drifting = False
        else:
            if self.moving_right:
                if abs(self.vel.x) < 1:
                    self.acc.x = 0
                    self.moving_right = False
                    self.drifting = True
                else:
                    self.acc.x = -ACC
            elif self.moving_left:
                if abs(self.vel.x) < 1:
                    self.acc.x = 0
                    self.moving_left = False
                    self.drifting = True
                else:
                    self.acc.x = ACC
        if self.drifting and abs(self.vel.x) < 1:
            self.vel.x = 0
        elif self.vel.x > MAX_SPEED:
            self.vel.x = MAX_SPEED
        elif self.vel.x < MAX_SPEED*-1:
            self.vel.x = MAX_SPEED*-1
        else:
            self.vel.x += self.acc.x
        
        # --== move y ==--
        if self.pressed_keys[K_SPACE]:
            if self.air_timer < 6:
                self.vel.y = -10
        self.vel.y += self.acc.y

        self.rect, self.collisions = move(self.rect, self.vel, player=True)
        if self.collisions["bottom"]:
            self.vel.y = 0
            self.air_timer = 0
        else:
            self.air_timer += 1
# -------------------------------------------------- Main game loop -------------------------------------------------------------------
player1 = Player()

while True:
    # --== Checking for events ==--
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    # --== Rendering objects on the screen ==--
    screen.fill(NIGHT_BLUE)
    platform()
    player1.update()
    screen.blit(player1.surf, player1.rect)
    # --== Updating the displays ==--
    pygame.display.update()
    frame_per_tick.tick(FPS)