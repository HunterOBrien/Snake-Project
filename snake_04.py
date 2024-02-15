""" v4
    adds the apple which will respawn if the snake head location is == to the apple location
    adds main menu to play again or quit
"""
import pygame
import time
import random

pygame.init()

game_icon = pygame.image.load('images/snake_icon.png')
pygame.display.set_icon(game_icon)
pygame.display.set_caption("Snake game - by Patrick Baker")
screen = pygame.display.set_mode((1000, 720))

# Colour hex codes
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (188, 227, 199)
yellow = (255, 255, 0)

# Game Fonts
score_font = pygame.font.SysFont("arialblack", 20)
exit_font = pygame.font.SysFont("freesansbold.ttf", 30)
msg_font = pygame.font.SysFont("arialblack", 20)

clock = pygame.time.Clock()  # Sets the speed for the snake to move


def message(msg, txt_colour, bkgd_colour):
    txt = msg_font.render(msg, True, txt_colour, bkgd_colour)

    # Center rect 1000/2, 720/2
    text_box = txt.get_rect(center=(500, 360))
    screen.blit(txt, text_box)


def game_loop():
    quit_game = False
    game_over = False

    # snake is 20 x 20 pixels at start
    snake_x = 490  # (1000 -20) /2  snake is 20pixels so taken away before finding middle value
    snake_y = 350  # (720 -20) /2  snake is 20pixels so taken away before finding middle value

    snake_x_change = 0  # Variable for change in x-coord per movement
    snake_y_change = 0  # Variable for change in y-coord per movement

    food_x = round(random.randrange(20, 1000 - 20) / 20) * 20
    food_y = round(random.randrange(20, 720 - 20) / 20) * 20

    quit_game = False
    while not quit_game:
        # Repeatability
        while game_over:
            screen.fill(white)
            message("You Died! Press Backspace to Quit or Enter to Continue!", black, white)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        quit_game = True
                        game_over = False
                    if event.key == pygame.K_RETURN:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game = True

            # Checks for WASD or Up,Down,Left,Right then adds to snake x,y change variables
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    snake_x_change = -20
                    snake_y_change = 0
                elif event.key == pygame.K_RIGHT:
                    snake_x_change = 20
                    snake_y_change = 0
                elif event.key == pygame.K_UP:
                    snake_x_change = 0
                    snake_y_change = -20
                elif event.key == pygame.K_DOWN:
                    snake_x_change = 0
                    snake_y_change = 20

        # If snake goes out of bounds game finishes
        if snake_x > 1000 or snake_x < 0 or snake_y >= 720 or snake_y < 0:
            game_over = True

        snake_x += snake_x_change
        snake_y += snake_y_change

        screen.fill(green)

        pygame.draw.rect(screen, red, [snake_x, snake_y, 20, 20])
        pygame.display.update()

        pygame.draw.circle(screen, yellow, [food_x, food_y], 10)
        pygame.display.update()

        # Collision detection (Test if snake touches food)
        if snake_x == food_x - 10 and snake_y == food_y - 10:
            # Sets new food pos
            food_x = round(random.randrange(20, 1000 - 20) / 20) * 20
            food_y = round(random.randrange(20, 720 - 20) / 20) * 20

        clock.tick(5)

    pygame.quit()
    quit()


game_loop()
