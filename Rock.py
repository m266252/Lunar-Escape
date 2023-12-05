import pygame
import random
from Game_Parameters import *

class Rock(pygame.sprite.Sprite):

    # Rocks fall from the sky function
    def __init__(self, x, y):
        super().__init__()

        # To scale the rock image and remove black rock background
        self.image = pygame.transform.scale(pygame.image.load("images/meteor.png"), (50, 50))
        self.image.set_colorkey((255, 255, 255))
        self.x = x
        self.y = y
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


    # Draw rocks on the screen
    def draw(self, scr):
        scr.blit(self.image, self.rect)

    # Make rocks move down the screen
    def update(self):
        self.y += 2
        self.rect.y = self.y

# Call all rocks as a group to appear on the screen
rocks = pygame.sprite.Group()

# Randomly spawn rocks across the game screen as they go off the screen
def add_rock(num_rocks):
    for _ in range(num_rocks):
        rocks.add(Rock(random.randint(0, screen_wid),
                       random.randint(-screen_hgt, 0)))

