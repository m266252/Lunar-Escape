import pygame
import time
import sys
from astro_man import Astro_man, Projectile, projectiles, player1
from Space_Girl import Space_Girl, player2
from Rock import *
from Hearts import *
from pygame import mixer


#Initializing Pygame
pygame.init()
pygame.mixer.init()

# Sets parameters for the screen
scr = pygame.display.set_mode((screen_wid, screen_hgt))

# Create menu screen.
background = pygame.image.load("images/moon1.png").convert()

#Create intro music on the menu screen
mixer.music.load('Sounds/intro_music.ogg')

# Create a play button
play = pygame.transform.scale(pygame.image.load('images/play_button.png'), (100,100)).convert()
play_button_rect = play.get_rect(midbottom= (screen_wid // 2, screen_hgt // 2 + 50))
play.set_colorkey((255, 255, 255))

# Create a rectangle for multiplayer option
multiplayer_rect = pygame.Rect((screen_wid // 2 - 110, screen_hgt // 2 + 65, 220, 50))

font = pygame.font.Font('Fonts/Black_Crayon.ttf', 35)
multiplayer_text = font.render("Multiplayer", True, (0,0,0)) # Black text
#multiplayer_rect = multiplayer_text.get_rect(midtop=(screen_wid // 2, play_button_rect.bottom + 30))


# Create a rectangle for Lunar Escape
lunar_escape_font = pygame.font.Font('Fonts/Black_Crayon.ttf', 70)
lunar_escape_text = lunar_escape_font.render('Lunar Escape', True, (0,0,0))
lunar_escape_rect = lunar_escape_text.get_rect(center=(screen_wid // 2, screen_hgt // 4))

MENU = "menu"
SINGLE = "singleplayer"
MULTIPLAYER = "multiplayer"
GAME_OVER = 'game_over'
current_state = MENU

# Play intro music after exiting the menu loop
mixer.music.load('Sounds/intro_music.ogg')
mixer.music.play()

stop_loop = False
while not stop_loop:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        #TODO: make two variations of collision points to go to either of the two game states
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if play_button_rect.collidepoint(event.pos):
                current_state = SINGLE
                stop_loop = True

            elif multiplayer_rect.collidepoint(event.pos):
                current_state = MULTIPLAYER
                stop_loop = True

        # Draw the menu screen with the play button
        scr.blit(background, (0,0))
        scr.blit(play, play_button_rect)
        scr.blit(lunar_escape_text, lunar_escape_rect)
        scr.blit(play, play_button_rect)
        scr.blit(multiplayer_text, multiplayer_rect)
        pygame.display.flip()

        # Small time delay
        time.sleep(0.10)

# Set image background
background = pygame.image.load("images/moon1.png").convert()
astro = Astro_man(400, 400)
sg = Space_Girl(500, 400)
player1.add(astro)
player2.add(sg)
add_rock(20)
add_heart(3)


#Initalize score
score = 0
sg_score = 0
score_font = pygame.font.Font('Fonts/Black_Crayon.ttf',30)

#Play background music
mixer.music.load('Sounds/background_music2.ogg')
mixer.music.play()

# Shooting sound upload
shoot_sound = pygame.mixer.Sound("Sounds/click_sound.ogg")

# Collision sounds
hit_sound = pygame.mixer.Sound('Sounds/hurt.ogg')

# Draw AM lives in the lower left corner
Life = 3
Life_icon = pygame.transform.scale(pygame.image.load('images/heart.png'), (30, 30)).convert()
Life_icon.set_colorkey((255, 255, 255))

# Draw SG lives in the lower right corner
SG_Life = 3
SG_Life_icon = pygame.transform.scale(pygame.image.load('images/heart.png'), (30, 30)).convert()
SG_Life_icon.set_colorkey((255, 255, 255))

#initialize timing
am_time_since_last_score = 0
am_time_since_last_heart = 0

sg_time_since_last_score = 0
sg_time_since_last_heart = 0

# Set time for game
clock = pygame.time.Clock()

# Text
my_font_1 = pygame.font.Font("Fonts/Brainfish_Rush.ttf",100)

# Game states
MENU = "menu"
SINGLE = "singleplayer"
MULTIPLAYER = "multiplayer"
GAME_OVER = 'game_over'
GAME_OVER_M = 'who won'


#Get mouse posiiton and check for events
mouse_pos = pygame.mouse.get_pos()


# Main loop
running = True
while running:
    if current_state == SINGLE:
        if Life == 0:
            current_state = GAME_OVER
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            mouse_pos = pygame.mouse.get_pos()

        # Shooting with left clicks and come from the center
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:              # Shoot with left clicks
                projectile = Projectile(astro.rect.x + 37, astro.rect.y + 37, *event.pos)
                projectiles.add(projectile)
                projectile.draw(scr)                          # Draws the projectile
                shoot_sound.play()                            #Plays the shooting sounds


        # Copy background to screen.
        scr.blit(background, (0, 0))

        # Check for projectile-rock collisions and remove rocks
        for projectile in projectiles:
            hit_rocks = pygame.sprite.spritecollide(projectile, rocks, True)
            if hit_rocks:
                projectiles.remove(projectile)

        # Draw American flag
        #flag.image = pygame.transform.scale(pygame.image.load('images/flag.png'),(40,40)).convert()
        #scr.blit(flag, (0, screen_wid - flag.get_height()))  # Adjust the position as needed

        # Updates position
        astro.update_position()
        rocks.update()
        projectiles.update()
        hearts.update()

        # Check if any rocks are off the screen
        for rock in rocks:
            if rock.rect.top > screen_hgt:
                rocks.remove(rock)
                add_rock(1)

        #Decrease lives as time passes
        current_time = pygame.time.get_ticks()
        if current_time - am_time_since_last_heart >= 100000:
            Life -= 1
            am_time_since_last_heart = current_time

        #Check for player collision with rocks
        hit_rocks = pygame.sprite.spritecollide(astro, rocks, True)
        if hit_rocks:
            Life -= 1
            hit_sound.play()
            print("Ouch! Life remaining:", Life)



        # Check for player collision with hearts
        result = pygame.sprite.spritecollide(astro, hearts, True)
        if result:
            Life += 1

        for heart in hearts:
            if heart.rect.top > screen_hgt:
                hearts.remove(heart)
                add_heart(1)

        #make score based on how long you survive
        current_time = pygame.time.get_ticks()
        if current_time - am_time_since_last_score >= 1000:
            score += 10
            am_time_since_last_score = current_time

        # Draw figures on the screen
        player1.draw(scr)
        rocks.draw(scr)
        projectiles.draw(scr)
        hearts.draw(scr)

        #draw hearts in the lower left corner
        for x in range(Life):
            scr.blit(Life_icon, (x * 34, (screen_hgt - 80)))

        #draw score in upper right
        text = score_font.render(f"SCORE : {score}", True, (255, 0, 0))
        scr.blit(text, (screen_wid//2, 10))

        # Show scr to user for 60 frames / second.
        pygame.display.flip()
        clock.tick(60)


    if current_state == MULTIPLAYER:
        if Life <= 0 and SG_Life <= 0:
            current_state = GAME_OVER_M
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            mouse_pos = pygame.mouse.get_pos()

        # Shooting with left clicks and come from the center
            if len(player1) == 1:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:              # Shoot with left clicks
                    projectile = Projectile(astro.rect.x + 37, astro.rect.y + 37, *event.pos)
                    projectiles.add(projectile)
                    projectile.draw(scr)                          # Draws the projectile
                    shoot_sound.play()                            #Plays the shooting sounds


        # Copy background to screen.
        scr.blit(background, (0, 0))

        # Check for projectile-rock collisions and remove rocks
        for projectile in projectiles:
            hit_rocks = pygame.sprite.spritecollide(projectile, rocks, True)
            if hit_rocks:
                projectiles.remove(projectile)

        # Draw American flag
        #flag.image = pygame.transform.scale(pygame.image.load('images/flag.png'),(40,40)).convert()
        #scr.blit(flag, (0, screen_wid - flag.get_height()))  # Adjust the position as needed

        # Updates position
        for player in player1:
            player.update_position()
        for player in player2:
            player.update_position()
        rocks.update()
        projectiles.update()
        hearts.update()

        # Check if any rocks are off the screen
        for rock in rocks:
            if rock.rect.top > screen_hgt:
                rocks.remove(rock)
                add_rock(1)

        #Decrease am lives as time passes
        current_time = pygame.time.get_ticks()
        if current_time - am_time_since_last_heart >= 100000:
            Life -= 1
            am_time_since_last_heart = current_time
        #Decrease sg lives as time passes
        current_time = pygame.time.get_ticks()
        if current_time - sg_time_since_last_heart >= 100000:
            SG_Life -= 1
            sg_time_since_last_heart = current_time

        #Check for player collision with rocks
        if Life > 0:
            hit_rocks = pygame.sprite.spritecollide(astro, rocks, True)
            if hit_rocks:
                Life -= 1
                hit_sound.play()
                print("Ouch! Life remaining:", Life)
                if Life <= 0:
                    astro.kill()

        if SG_Life > 0:
            hit_rocks = pygame.sprite.spritecollide(sg, rocks, True)
            if hit_rocks:
                SG_Life -= 1
                hit_sound.play()
                print("Ouch! Life remaining:", Life)
                if SG_Life <= 0:
                    sg.kill()


        # Check for player collision with hearts
        if Life > 0:
            result = pygame.sprite.spritecollide(astro, hearts, True)
            if result:
                Life += 1

        if Life > 0:
            result = pygame.sprite.spritecollide(sg, hearts, True)
            if result:
                SG_Life += 1

        for heart in hearts:
            if heart.rect.top > screen_hgt:
                hearts.remove(heart)
                add_heart(1)

        if len(hearts) < 1:
            add_heart(1)

        #make score based on how long you survive
        current_time = pygame.time.get_ticks()
        if len(player1) > 0:
            if current_time - am_time_since_last_score >= 1000:
                score += 10
                am_time_since_last_score = current_time

        if len(player2) > 0:
            current_time = pygame.time.get_ticks()
            if current_time - sg_time_since_last_score >= 1000:
                sg_score += 10
                sg_time_since_last_score = current_time

        # Draw figures on the screen
        player1.draw(scr)
        player2.draw(scr)
        rocks.draw(scr)
        projectiles.draw(scr)
        hearts.draw(scr)

        #draw am hearts in the lower left corner
        for x in range(Life):
            scr.blit(Life_icon, (x * 34, (screen_hgt - 80)))

        #draw sg hearts in the lower right corner
        for x in range(SG_Life):
            scr.blit(Life_icon, (screen_wid - 34 * (x+1), screen_hgt - 80))

        #draw am score in upper left
        text = score_font.render(f"SCORE : {score}", True, (255, 0, 0))
        scr.blit(text, (10, 10))

        #draw sg score in the upper right
        sg_text = score_font.render(f"SCORE : {sg_score}", True, (0, 0, 0))
        scr.blit(sg_text, (screen_wid//2 + 200, 10))

        # Show scr to user for 60 frames / second.
        pygame.display.flip()
        clock.tick(60)

    if current_state == GAME_OVER:
        print('single player game over')
        # show game over message and their final game score
        message = score_font.render("GAME OVER!!", True, (255, 0, 0))
        scr.blit(message, (screen_wid / 2 - message.get_width() / 2, screen_hgt / 2))
        score_text = score_font.render(f"Score: {score} ", True, (0, 0, 0))
        scr.blit(score_text,
                 (screen_wid / 2 - score_text.get_width() / 2, screen_hgt / 2 - 2 * score_text.get_height() / 2))
        # Wait for a key press to return to the menu
        pygame.display.flip()
        key_pressed = False
        while not key_pressed:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:        #enter key
                        current_state = MENU
                        key_pressed = True

        # update the display
        pygame.display.flip()

        # play game over sound effect
        game_over = pygame.mixer.Sound("Sounds/game_over.ogg")
        game_over.play()


    if current_state == GAME_OVER_M:
        print('multiplayer game over')
        # show game over message and their final game score
        if score > sg_score:
            message = score_font.render("ASTRO MAN WINS!!", True, (255, 0, 0))
            scr.blit(message, (screen_wid / 2 - message.get_width() / 2, screen_hgt / 2))
            score_text = score_font.render(f"Score: {score} ", True, (0, 0, 0))
            scr.blit(score_text,
                     (screen_wid / 2 - score_text.get_width() / 2, screen_hgt / 2 - 2 * score_text.get_height() / 2))
        elif score < sg_score:
            message = score_font.render("SPACE GIRL WINS!!", True, (255, 0, 0))
            scr.blit(message, (screen_wid / 2 - message.get_width() / 2, screen_hgt / 2))
            score_text = score_font.render(f"Score: {sg_score} ", True, (0, 0, 0))
            scr.blit(score_text,
                     (screen_wid / 2 - score_text.get_width() / 2, screen_hgt / 2 - 2 * score_text.get_height() / 2))

        else:
            message = score_font.render("DRAW!!", True, (255, 0, 0))
            scr.blit(message, (screen_wid / 2 - message.get_width() / 2, screen_hgt / 2))
            score_text = score_font.render(f"Score: {score} ", True, (0, 0, 0))
            scr.blit(score_text,
                     (screen_wid / 2 - score_text.get_width() / 2, screen_hgt / 2 - 2 * score_text.get_height() / 2))

        # Wait for a key press to return to the menu
        pygame.display.flip()
        key_pressed = False
        while not key_pressed:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:        #enter key
                        current_state = MENU
                        key_pressed = True

        # update the display
        pygame.display.flip()

        # play game over sound effect
        game_over = pygame.mixer.Sound("Sounds/game_over.ogg")
        game_over.play()

    if current_state == MENU:
        print('menu')


#update the display
pygame.display.flip()

#play game over sound effect
game_over = pygame.mixer.Sound("Sounds/game_over.ogg")
game_over.play()




#wait for user to exit the game
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
















