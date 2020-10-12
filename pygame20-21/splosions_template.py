import pygame
from pygame.locals import *
import sys

pygame.init()

FPS = 60
WIDTH = 500
HEIGHT = 500
ORANGE = (224, 129, 13)
frame_per_sec = pygame.time.Clock()

displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Splosions!")
displaysurface.fill((255, 255, 255))

class splosion():
    def __init__(self):
        """
        Hvilke variabler trenger vi? De bør vi initieres i denne metoden
        """
        pass

    def draw(self, pos):
        """
        for å tegne en sirkel bruk funksjonen pygame.draw.circle(surface, farge, posisjon, radius, linetykkelse)
        hvor surface er pygame-flaten du vil tegne på (i vårt tilfelle har vi kalt hovedflaten for
        displaysurface).
        
        Argumentet (parameteren) pos skal vi bruke som posisjonen til sirkelen vi vil tegne
        """
        pass

    def update(self, pos):
        """
        Hva skal skje med sirkelen når den oppdateres? Jo den skal vokse, og linjestørrelsen bli mindre
        Hva må vi gjøre med variablene for å få til det?
        """
        pass


while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == MOUSEBUTTONDOWN:
            """
            Vi må lage en instanse av splosion()-klassen. Hvis vi vil ha flere sirkler må vi ha en liste med instanser
            Vi kan hente musepekerens posisjon med : pygame.mouse.get_pos() - denne kan vi lagre i en variabel,
            eller en liste med flere posisjoner (hvis vi vil ha flere sirkler)
            """
            pass

    
    pygame.display.update()
    frame_per_sec.tick(FPS)