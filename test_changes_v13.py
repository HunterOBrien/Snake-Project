""" v11

"""
import pygame
import time
import random

pygame.init()

game_icon = pygame.image.load('images/snake_icon.png')
pygame.display.set_icon(game_icon)
pygame.display.set_caption("Snake game - by Patrick Baker")
screen = pygame.display.set_mode((340, 300), pygame.RESIZABLE)


# Colour hex codes
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (188, 227, 199)
yellow = (255, 255, 0)

# Game Fonts
score_font = pygame.font.SysFont("snake chan.ttf", 20)
exit_font = pygame.font.SysFont("freesansbold.ttf", 30)
msg_font = pygame.font.SysFont("arialblack", 20)

clock = pygame.time.Clock()  # Sets the speed for the snake to move


# saves updated highscore
def save_high_score(high_score):
    high_score_file = open("HI_score.txt", 'w')
    high_score_file.write(str(high_score))
    high_score_file.close()


# Function to update recorded highscore
def update_high_score(score, highscore):
    if int(score) > int(highscore):
        return score
    else:
        return highscore


# Function to save highscore in a separate file
def load_high_score():
    try:
        hi_score_file = open("HI_score.txt", 'r')
    except IOError:
        hi_score_file = open("HI_score.txt", 'w')
        hi_score_file.write("0")
    hi_score_file = open("HI_score.txt", 'r')
    value = hi_score_file.read()
    hi_score_file.close()
    return value


# Display player score during the game
def player_score(score, score_colour, hi_score):
    display_score = score_font.render(f"Score: {score}", True, score_colour)
    screen.blit(display_score, (270, 20))  # Coordinates for top right

    # Hi score
    display_score = score_font.render(f"High Score: {hi_score}", True, score_colour)
    screen.blit(display_score, (10, 10))  # Coordinates for top left


# Create snake, replaces the previous snake in main loop
def draw_snake(snake_list):
    for i in snake_list:
        pygame.draw.rect(screen, red, [i[0], i[1], 20, 20])


def message(msg, txt_colour, bkgd_colour):
    txt = msg_font.render(msg, True, txt_colour, bkgd_colour)

    # Center rect 340/2, 300/2
    text_box = txt.get_rect(center=(170, 150))
    screen.blit(txt, text_box)


def game_loop():
    quit_game = False
    game_over = False

    # classic snake game 17 x 15 tiles
    # snake is 20 x 20 pixels at start
    snake_x = 160  # (340 -20) /2  snake is 20pixels so taken away before finding middle value
    snake_y = 140  # (300 -20) /2  snake is 20pixels so taken away before finding middle value

    snake_x_change = 0  # Variable for change in x-coord per movement
    snake_y_change = 0  # Variable for change in y-coord per movement
    snake_list = []
    snake_length = 1

    food_x = round(random.randrange(20, 340 - 20) / 20) * 20
    food_y = round(random.randrange(20, 300 - 20) / 20) * 20

    # Loads highscore
    high_score = load_high_score()

    quit_game = False
    while not quit_game:
        while game_over:
            save_high_score(high_score)
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

        # if user presses x gives them option to quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

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
        if snake_x > 320 or snake_x < 0 or snake_y >= 280 or snake_y < 0:
            game_over = True

        snake_x += snake_x_change
        snake_y += snake_y_change

        screen.fill(green)

        # Creates snake (replacing  20x20 rectangle)
        snake_head = [snake_x, snake_y]
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]

        # Detects if snake head touches any other part (-1 counts from the end of list)
        for x in snake_list[:-1]:
            if x == snake_head:
                game_over = True

        draw_snake(snake_list)

        # Keeps track of player score
        score = snake_length - 1  # excludes snake head
        player_score(score, black, high_score)

        # Get highscore
        high_score = update_high_score(score, high_score)

        # Links speed of snake to player score to increase difficulty
        if score > 3:
            speed = score
        else:
            speed = 3

        # Uses a sprite instead of previous circle to represent food
        food = pygame.Rect(food_x, food_y, 20, 20)
        apple = pygame.image.load('images/apple_3.png').convert_alpha()
        resized_apple = pygame.transform.smoothscale(apple, [20, 20])
        screen.blit(resized_apple, food)

        pygame.display.update()

        # Collision detection (Test if snake touches food)
        if snake_x == food_x and snake_y == food_y:
            # Sets new food pos
            food_x = round(random.randrange(20, 340 - 20) / 20) * 20
            food_y = round(random.randrange(20, 300 - 20) / 20) * 20

            # Increase length of snake when collision with apple
            snake_length += 1

        clock.tick(speed)

    pygame.quit()
    quit()


game_loop()
