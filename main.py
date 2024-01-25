import pygame
from snake import *
from random import randint
pygame.init()

SQUARE_SIZE=40
BOARD_LENGTH=15
BOARD_HEIGHT=15
WHITE,BLACK= (98,255,92),(69,232,63)

SNAKE_COLOR=(30,144,255)
APPLE_COLOR=(255,0,0)
gameDisplay = pygame.display.set_mode((1240, 600))
gameDisplay.fill(WHITE)


def main():
    score=0
    global my_snake
    my_snake=snake()
    apple = create_apple()
    while True:
        draw_board()
        draw_snake()
        while apple==-1:
            apple=create_apple()
        draw_apple(apple[0],apple[1])
        if snake_eating_apple(apple[0],apple[1]):
            apple=-1
            score+=1
        check_buttons_pressed()
        pygame.display.update()
        my_snake.move()
        pygame.time.delay(10)

def snake_eating_apple(apple_x,apple_y):
    snake_head=my_snake.get_head()
    apple_rect=pygame.Rect(apple_x,apple_y,SQUARE_SIZE,SQUARE_SIZE)
    snake_head_rect=pygame.Rect(snake_head.get_pos_x(),snake_head.get_pos_y(),SQUARE_SIZE,SQUARE_SIZE)
    return apple_rect.colliderect(snake_head_rect)

def create_apple():
    apple_x=randint(0,BOARD_LENGTH-1)*SQUARE_SIZE
    apple_y=randint(0,BOARD_HEIGHT-1)*SQUARE_SIZE
    if apple_inside_snake(apple_x,apple_y):
        return -1
    return apple_x,apple_y

def apple_inside_snake(apple_x,apple_y):
    apple_rect = pygame.Rect(apple_x, apple_y, SQUARE_SIZE, SQUARE_SIZE)
    snake_blocks = my_snake.get_blocks()
    for block in snake_blocks:
        block_rect=pygame.Rect(block.get_pos_x(),block.get_pos_y(),SQUARE_SIZE,SQUARE_SIZE)
        if apple_rect.colliderect(block_rect):
            return True
    return False
def check_buttons_pressed():
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:
            respond_to_button_pressed(event.key)


def respond_to_button_pressed(button_pressed):
    cur_dir = my_snake.get_direction()
    new_dir=""
    match button_pressed:
        case pygame.K_UP:
            new_dir = "up"
        case pygame.K_DOWN:
            new_dir = "down"
        case pygame.K_RIGHT:
            new_dir = "right"
        case pygame.K_LEFT:
            new_dir = "left"
        case _:
            return

    my_snake.add_turn(new_dir)

def draw_snake():
    blocks=my_snake.get_blocks()
    for block in blocks:
        pygame.draw.rect(gameDisplay, SNAKE_COLOR, [block.get_pos_x(), block.get_pos_y(), SQUARE_SIZE, SQUARE_SIZE])

def draw_board():
    color = 0
    for x in range(BOARD_HEIGHT):
        for y in range(BOARD_LENGTH):
            if color %2 == 0:
                pygame.draw.rect(gameDisplay, WHITE,[SQUARE_SIZE*y,SQUARE_SIZE*x,SQUARE_SIZE,SQUARE_SIZE])
            else:
                pygame.draw.rect(gameDisplay, BLACK, [SQUARE_SIZE * y, SQUARE_SIZE * x, SQUARE_SIZE, SQUARE_SIZE])
            color += 1

def draw_apple(apple_x,apple_y):
    pygame.draw.rect(gameDisplay, APPLE_COLOR, [apple_x, apple_y, SQUARE_SIZE, SQUARE_SIZE])

main()