"""

"""
import pygame
import time

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

# Game Fonts
score_font = pygame.font.SysFont("arialblack", 20)
exit_font = pygame.font.SysFont("freesansbold.ttf", 30)

# snake is 20 x 20 pixels at start
snake_x = 490  # (1000 -20) /2  snake is 20pixels so taken away before finding middle value
snake_y = 350  # (720 -20) /2  snake is 20pixels so taken away before finding middle value

clock = pygame.time.Clock()  # Sets the speed for the snake to move

snake_x_change = 0  # Variable for change in x-coord per movement
snake_y_change = 0  # Variable for change in y-coord per movement

quit_game = False
while not quit_game:
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

    snake_x += snake_x_change
    snake_y += snake_y_change

    screen.fill(green)

    pygame.draw.rect(screen, red, [snake_x, snake_y, 20, 20])
    pygame.display.update()

    clock.tick(5)

pygame.quit()
quit()
