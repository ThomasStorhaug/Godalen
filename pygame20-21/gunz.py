import pygame, sys, random, math
from pygame.locals import *

pygame.init()
vec = pygame.math.Vector2

FPS = 60

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

WIDTH = 500
HEIGHT = 500

screen = pygame.display.set_mode((WIDTH, HEIGHT))
frame_per_tick = pygame.time.Clock()

tenth_update = pygame.USEREVENT
pygame.time.set_timer(tenth_update, 100)

EFFECTS_SURFACE = pygame.Surface((WIDTH, HEIGHT))
EFFECTS_SURFACE.set_colorkey(BLACK)
EF_RECT = EFFECTS_SURFACE.get_rect()

# ------------------------------------ Particles ------------------------------------------------------------------
#
# particle = [pos, velocity, timer]
#
#
particles = []

def particle_gen(surf, pos=None):
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

            pygame.draw.circle(surf, LASER_CORE, (int(part[0][0]), int(part[0][1])), int(part[2]))

def laser(surf, start_pos, aimed_pos):
    m_x, m_y = aimed_pos
    g_x, g_y = start_pos
    theta_0 = math.degrees(math.atan((HEIGHT-g_y)/(WIDTH-g_x)))
    if m_x == g_x:
        theta = 90
    elif m_x > g_x:
        theta = math.degrees(math.atan((g_y-m_y)/abs(m_x-g_x)))
    else:
        theta = 180 - math.degrees(math.atan((g_y-m_y)/abs(m_x-g_x)))
    if theta == 0:
        end_y = g_y
        end_x = WIDTH - 1
    elif 0 < theta < theta_0:
        end_y = g_y - abs(math.tan(math.radians(theta)))*WIDTH/2 + 1
        end_x = WIDTH - 1
    elif theta_0 <= theta < 90:
        end_y = 1
        end_x = HEIGHT/math.tan(math.radians(theta)) + g_x - 1
    elif 90 <= theta < 180 - theta_0:
        end_y = 1
        end_x = g_x - g_y/math.tan(math.radians(180 - theta)) + 1
    elif 180 - theta_0 < theta < 180:
        end_y = g_y -  math.tan(math.radians(180-theta))*g_x
        end_x = 1
    elif theta_0*(-1) < theta < 0:
        end_y = g_y + math.tan(math.radians(theta))*(WIDTH - g_x)*(-1) + 1
        end_x = WIDTH - 1
    else:
        end_y = HEIGHT - 1
        end_x = (HEIGHT - g_y)/math.tan(math.radians(theta*(-1))) + g_x + 1
    
    end_pos = (end_x, end_y)
    pygame.draw.line(surf, LASER_SHADOW, start_pos, (end_x, end_y), random.randint(7, 9))
    pygame.draw.line(surf, LASER_RED, start_pos, (end_x, end_y), random.randint(3, 5))
    pygame.draw.line(surf, LASER_CORE, start_pos, (end_x, end_y), random.randint(1, 3))
    
    return end_pos

class Gun():
    def __init__(self):
        self.update_index = 0
        self.gun_fired = False
        self.gun_sheet = pygame.image.load("superthomas/gun_sprite.png")
        self.gun_surf = pygame.Surface((32, 32))
        self.gun_rect = self.gun_surf.get_rect()
        self.gun_rect.center = (WIDTH/2, HEIGHT/2)

    def update(self):
        self.gun_surf.fill((0, 0, 0, 0))
        self.mousebuttons = pygame.mouse.get_pressed()

        self.aimed_pos = pygame.mouse.get_pos()
        self.gun_pos = (WIDTH/2, HEIGHT/2)
        if self.aimed_pos[0] == self.gun_pos[0]:
            self.theta = 90
        elif self.aimed_pos[0] > self.gun_pos[0]:
            self.theta = math.degrees(math.atan((self.gun_pos[1]-self.aimed_pos[1])/abs(self.aimed_pos[0]-self.gun_pos[0])))
        else:
            self.theta = 180 - math.degrees(math.atan((self.gun_pos[1]-self.aimed_pos[1])/abs(self.aimed_pos[0]-self.gun_pos[0])))
        EFFECTS_SURFACE.fill((0, 0, 0, 0))
        # -------------------------------------- when mouseclicked -----------------------------------------------------------------
        
        if self.mousebuttons[0]:
            self.sprite = (32, 0, 32, 32)
            self.gun_fired = True
            laser(EFFECTS_SURFACE, self.gun_pos, self.aimed_pos)
            self.part_pos = laser(EFFECTS_SURFACE, self.gun_pos, self.aimed_pos)
            self.p_x, self.p_y = self.part_pos
            particle_gen(EFFECTS_SURFACE, [self.p_x, self.p_y])
        else:
            if self.gun_fired:
                self.sprite = (32 + 32*self.update_index, 0, 32, 32)
            else:
                self.sprite = (0, 0, 32, 32)
            particle_gen(EFFECTS_SURFACE)
        
        self.gun_surf.blit(self.gun_sheet, (0, 0), self.sprite)
        self.gun_surf.set_colorkey(BLACK)
        
        if self.theta <= 90:
            self.gun_surf_r = pygame.transform.rotate(self.gun_surf, self.theta)
            self.rect = self.gun_surf_r.get_rect()
            self.rect.center = (WIDTH/2, HEIGHT/2)
        else:
            self.gun_surf_f = pygame.transform.flip(self.gun_surf, False, True)
            self.gun_surf_r = pygame.transform.rotate(self.gun_surf_f, self.theta)
            self.rect = self.gun_surf_r.get_rect()
            self.rect.center = (WIDTH/2, HEIGHT/2)
        

gun1 = Gun()
trigger_release = False
while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONUP:
            trigger_release = True
        elif event.type == MOUSEBUTTONDOWN:
            trigger_release = False
        if event.type == tenth_update:
            if gun1.gun_fired and trigger_release:
                if gun1.update_index == 4:
                    gun1.gun_fired = False
                else:
                    gun1.update_index += 1
    gun1.update()
    screen.fill(NIGHT_BLUE)
    screen.blit(EFFECTS_SURFACE, EF_RECT)
    screen.blit(gun1.gun_surf_r, gun1.rect)
    pygame.display.update()
    frame_per_tick.tick(FPS)