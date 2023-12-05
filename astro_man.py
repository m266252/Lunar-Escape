import math
import pygame
import random
from Game_Parameters import *

screen_wid = 800
screen_hgt = 600


class Astro_man(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()

        # Astronaut character
        self.image = pygame.image.load('images/astro20.png').convert()
        self.image.set_colorkey((255, 255, 255))


        #Change scale and remove white box behind Astro man
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.astro_spd = 2
        self.rect.center = (x, y)

        #Sets the speed for astro man
        self.astro_x_spd = self.astro_spd
        self.astro_y_spd = self.astro_spd

        # Sounds.
        #self.chomp = pygame.mixer.Sound('assests/sounds/chomp.wav')

    def draw(self, scr):
        # Draws Astro man on to the screen
        scr.blit(self.image, self.rect)



    # Function that allows Astro man to move left, right, up and down
    def update_position(self):

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= self.astro_x_spd
        if keys[pygame.K_d] and self.rect.right < screen_wid:
            self.rect.x += self.astro_x_spd
        if keys[pygame.K_s] and self.rect.bottom < screen_hgt:
            self.rect.y += self.astro_y_spd
        if keys[pygame.K_w] and self.rect.top > 0:
            self.rect.y -= self.astro_y_spd



class Projectile(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y, target_x, target_y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('images/blue_planet.png'),(40,40)).convert()
        self.image.set_colorkey((0,0,0))                    #Remove the white background behind the sprite
        self.rect = self.image.get_rect()                    # Making the rectangle for the image
        self.rect.center = (start_x, start_y)
        self.target_x = target_x
        self.target_y = target_y
        self.spd = 7


    def rock_collisions(self, rock_group):
        return pygame.sprite.spritecollide(self, rock_group, True)


    def update(self):

        if self.rect.colliderect(pygame.Rect(self.target_x - 5, self.target_y - 5, 10, 10)):
            self.kill()
        else:
            # Calculate the angle between the projectile and the target
            angle = math.atan2(self.target_y - self.rect.centery, self.target_x - self.rect.centerx)

            # Calculate the velocity componenets
            velocity_x = self.spd * math.cos(angle)
            velocity_y = self.spd * math.sin(angle)

            # Update the projectiles position based on velocity
            self.rect.x += velocity_x
            self.rect.y += velocity_y


    def draw(self,surface):
        # Draws the projectile on the screen
        surface.blit(self.image, self.rect.center)


# Establish projectiles and AM as group sprites
projectiles = pygame.sprite.Group()
player1 = pygame.sprite.Group()