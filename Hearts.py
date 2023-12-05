import pygame
import random
from Game_Parameters import *

# Establish heart class and parameters
class Heart(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("images/heart.png"), (25, 25)).convert()
        self.image.set_colorkey((255, 255, 255))  # Set white color as transparent
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.center = (x, y)


    # Adjusts speed and movement down the game screen
    def update(self):
        self.y += 1
        self.rect.y = self.y


    #Blit the hearts on to the game screen
    def draw(self, surface):
        surface.blit(self.image, self.rect)

# Establish hearts as a group
hearts = pygame.sprite.Group()

# Hearts randomly spawn across the x plane
def add_heart(num_heart):
    for x in range(num_heart):
        hearts.add(Heart(random.randint(0, screen_wid),
                         random.randint(0, screen_hgt)))

# Add new hearts on to the game screen once all gone
def add_hearts(num_hearts):
    for _ in range(num_hearts):
        x = random.randint(0, screen_wid)
        y = random.randint(0, screen_hgt)
        heart = Heart(x, y)  # Pass x and y when creating a new heart instance
        hearts.add(heart)


