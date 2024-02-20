""" Testing v4
    Added Message to Welcome/Death screen
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

# Game Fonts
score_font = pygame.font.SysFont("snake chan.ttf", 20)
exit_font = pygame.font.SysFont("freesansbold.ttf", 30)
msg_font = pygame.font.SysFont("arialblack", 20)


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


def game_loop():
    global game_over
    game_over = False

    # snake is 20 x 20 pixels at start
    snake_x = round((game_screen_width - 40) / 2 / 40) * 40
    snake_y = round((game_screen_height - 40) / 2 / 40) * 40

    snake_x_change = 0  # Variable for change in x-coord per movement
    snake_y_change = 0  # Variable for change in y-coord per movement
    snake_list = []
    snake_length = 1

    food_x = round(random.randrange(0, game_screen_width - 40) / 40) * 40
    food_y = round(random.randrange(0, game_screen_height - 40) / 40) * 40
    # Loads highscore
    high_score = load_high_score()

    quit_game = False
    while not quit_game:
        while game_over:
            save_high_score(high_score)
            game_screen.fill(white)
            pygame.display.update()

            welcome_screen()

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

        snake_x += snake_x_change
        snake_y += snake_y_change

        # Check for collision with boundary walls
        if (snake_x < 0 or snake_x >= game_screen_width or
                snake_y < 0 or snake_y >= game_screen_height):
            welcome_screen()

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

        draw_snake(snake_list)

        # Keeps track of player score
        score = snake_length - 1  # excludes snake head
        player_score(score, black, high_score)

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

        # Get highscore
        high_score = update_high_score(score, high_score)

        game_screen.fill(white)
        draw_snake(snake_list)

        # Display food
        pygame.draw.rect(game_screen, green, [food_x, food_y, 40, 40])

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



def quit_game():
    pygame.quit()
    quit()


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
    game_screen.blit(display_score, (800, 20))  # Coordinates for top right

    # Hi score
    display_score = score_font.render(f"High Score: {hi_score}", True, score_colour)
    game_screen.blit(display_score, (10, 10))  # Coordinates for top left


def welcome_screen():
    welcome_message = "Welcome to the Snake Game! Press Enter to start. Backspace to Quit"
    welcome_font = pygame.font.Font(None, 36)
    text_surface = welcome_font.render(welcome_message, True, white)
    text_rect = text_surface.get_rect(center=(full_screen_size[0] // 2, full_screen_size[1] // 2))

    welcome = True
    while welcome:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    quit_game()
                elif event.key == pygame.K_RETURN:
                    welcome = False  # Exit the loop when Enter key is pressed
                    game_loop()

        main_screen.blit(background_screen, (10, 10))
        # Draw the welcome message on the screen
        main_screen.blit(text_surface, text_rect)

        pygame.display.update()
        clock.tick(15)


welcome_screen()
