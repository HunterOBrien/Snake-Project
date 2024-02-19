""" Testing v2
    Modified screen to have different surfaces allowing for background
    as well as game screen
"""

import pygame
import time
import random

pygame.init()

dark_green = (5, 55, 37)
white = (255, 255, 255)
black = (0, 0, 0)

game_screen_width = 680  # 17 tiles * 20 pixel snake * 2 (bigger screen)
game_screen_height = 600  # 15 tiles * 20 pixel snake * 2 (bigger screen)

# Finds out size of users device screen
display_info = pygame.display.Info()
full_screen_size = (display_info.current_w, display_info.current_h)

# Sets main screen
main_screen = pygame.display.set_mode(full_screen_size)
main_screen.fill(black)

# Calculate the position to center the game screen
game_screen_x = (full_screen_size[0] - game_screen_width) // 2
game_screen_y = (full_screen_size[1] - game_screen_height) // 2

# background_screen = pygame.surface((background_screen_size))
game_screen = pygame.Surface((game_screen_width, game_screen_height))
game_screen.fill(white)

# Creates background screen using full screen size information
background_screen = pygame.Surface((display_info.current_w - 20, display_info.current_h - 20))
background_screen.fill(dark_green)

quit_game = False
while not quit_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game = True

    main_screen.blit(background_screen, (10, 10))
    main_screen.blit(game_screen, (game_screen_x, game_screen_y))

    pygame.display.flip()

pygame.quit()
quit()
