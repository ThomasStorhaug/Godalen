import pygame
from pygame.locals import *
import sys

pygame.init()

WIDTH = 500
HEIGHT = 500
ORANGE = (224, 129, 13)
frame_per_sec = pygame.time.Clock()

displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Splosions!")
displaysurface.fill((255, 255, 255))

class splosion():
    def __init__(self):
        self.radius = 10
        self.line_width = 10
        

    def draw(self, pos):
        self.pos = pos
        pygame.draw.circle(displaysurface, ORANGE, self.pos, self.radius, self.line_width)
        print("circle")

    def update(self, pos):
        self.pos = pos
        if self.radius <= 200:
            self.radius += 5
            if self.radius % 20 == 0 and self.line_width -1 != 0:
                self.line_width -= 1
            pygame.draw.circle(displaysurface, ORANGE, self.pos, self.radius, self.line_width)
splosion_list = []
number_of_splosions = 0
position_list = []
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            position_list.append(pygame.mouse.get_pos())
            splosion_list.append(splosion())
            number_of_splosions += 1
            pygame.display.update()
    displaysurface.fill((255, 255, 255))

    if len(position_list) >= 1:
        for iterator, splo in enumerate(splosion_list):
            splo.update(position_list[iterator])

    pygame.display.update()
    frame_per_sec.tick(60)