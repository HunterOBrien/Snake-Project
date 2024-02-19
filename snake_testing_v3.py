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
red = (255, 0, 0)
green = (188, 227, 199)

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

clock = pygame.time.Clock()  # Sets the speed for the snake to move


# Create snake, replaces the previous snake in main loop
def draw_snake(snake_list):
    for i in snake_list:
        pygame.draw.rect(game_screen, red, [i[0], i[1], 40, 40])


def welcome_screen():
    welcome = True
    while welcome:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
        main_screen.blit(background_screen, (10, 10))
        # Add welcome screen elements
        # Example: You can draw a welcome message, instructions, etc.
        pygame.display.update()
        clock.tick(15)


def game_loop():
    quit_game = False
    game_over = False

    welcome_screen()

    # snake is 20 x 20 pixels at start
    # snake_x = game_screen_width / 2  # (1000 - 40) /2  snake is 40 pixels so taken away before finding middle value
    # snake_y = game_screen_height / 2  # (720 -20) /2  snake is 40 pixels so taken away before finding middle value
    snake_x = round((game_screen_width - 40) / 2 / 40) * 40
    snake_y = round((game_screen_height - 40) / 2 / 40) * 40

    snake_x_change = 0  # Variable for change in x-coord per movement
    snake_y_change = 0  # Variable for change in y-coord per movement
    snake_list = []
    snake_length = 1

    food_x = round(random.randrange(0, game_screen_width - 40) / 40) * 40
    food_y = round(random.randrange(0, game_screen_height - 40) / 40) * 40

    quit_game = False
    while not quit_game:
        while game_over:
            game_screen.fill(white)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        quit_game = True
                        game_over = False
                    if event.key == pygame.K_RETURN:
                        game_loop()

        # if user presses x gives them option to quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            # Checks for WASD or Up,Down,Left,Right then adds to snake x,y change variables
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    snake_x_change = -40
                    snake_y_change = 0
                elif event.key == pygame.K_RIGHT:
                    snake_x_change = 40
                    snake_y_change = 0
                elif event.key == pygame.K_UP:
                    snake_x_change = 0
                    snake_y_change = -40
                elif event.key == pygame.K_DOWN:
                    snake_x_change = 0
                    snake_y_change = 40

        # If snake goes out of bounds game finishes
        # if snake_x > game_screen_x + 680 or snake_x < game_screen_x or snake_y >=
        # game_screen_y + 600 or snake_y < game_screen_y:
        # game_over = True

        snake_x += snake_x_change
        snake_y += snake_y_change

        # Check for collision with boundary walls
        if (snake_x < 0 or snake_x >= game_screen_width or
                snake_y < 0 or snake_y >= game_screen_height):
            game_over = True

        # SCREEN
        main_screen.blit(background_screen, (10, 10))
        main_screen.blit(game_screen, (game_screen_x, game_screen_y))
        pygame.display.update()

        # Creates snake (replacing  20x20 rectangle)
        snake_head = [snake_x, snake_y]
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]

        # Detects if snake head touches any other part (-1 counts from the end of list)
        for x in snake_list[:-1]:
            if x == snake_head:
                game_over = True

        game_screen.fill(white)
        draw_snake(snake_list)
        pygame.display.update()

        # Keeps track of player score
        score = snake_length - 1  # excludes snake head

        # Links speed of snake to player score to increase difficulty
        if score > 10:
            speed = 4.5
        else:
            speed = 3.8

        # Uses a sprite instead of previous circle to represent food
        food = pygame.Rect(food_x, food_y, 0, 0)
        apple = pygame.image.load('images/apple_3.png').convert_alpha()
        resized_apple = pygame.transform.smoothscale(apple, [40, 40])
        game_screen.blit(resized_apple, food)

        pygame.display.update()

        # Collision detection (Test if snake touches food)
        if snake_x == food_x and snake_y == food_y:
            # Sets new food pos
            food_x = round(random.randrange(0, game_screen_width - 40) / 40) * 40
            food_y = round(random.randrange(0, game_screen_height - 40) / 40) * 40

            # Increase length of snake when collision with apple
            snake_length += 1

        clock.tick(speed)

    pygame.quit()
    quit()


game_loop()
