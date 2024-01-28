import pygame
from snake import snake
from random import randint
from block import block
from constants import *

pygame.init()
gameDisplay = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
gameDisplay.fill(WHITE)

def main():
    score=0
    global my_snake
    my_snake=snake()
    apple = create_apple()
    prev_dir=""
    while True:
        draw_board()
        draw_snake()

        while apple==APPLE_INSIDE_SNAKE or apple==EATEN_APPLE:
            apple=create_apple()
        draw_apple(apple.get_pos_x(),apple.get_pos_y())


        if snake_eating_apple(apple.get_pos_x(),apple.get_pos_y()):
            prev_dir = my_snake.get_last_block().get_direction()
            my_snake.grow()
            apple=EATEN_APPLE
            score+=1

        pygame.display.update()
        check_buttons_pressed()
        my_snake.move()

        last_snake_block=my_snake.get_last_block()
        if last_snake_block.get_direction()=="":
            if distance_between_blocks(my_snake.blocks[-2],last_snake_block)>=SQUARE_SIZE:
                last_snake_block.turn(prev_dir)
        pygame.time.delay(TIME_DELAY)



def snake_eating_apple(apple_x,apple_y):
    snake_head=my_snake.get_head()
    apple_rect=pygame.Rect(apple_x,apple_y,SQUARE_SIZE,SQUARE_SIZE)
    snake_head_rect=pygame.Rect(snake_head.get_pos_x(),snake_head.get_pos_y(),SQUARE_SIZE,SQUARE_SIZE)
    return apple_rect.colliderect(snake_head_rect)

def create_apple():
    apple_x=randint(0,BOARD_LENGTH-1)*SQUARE_SIZE
    apple_y=randint(0,BOARD_HEIGHT-1)*SQUARE_SIZE
    if block_inside_snake(apple_x,apple_y):
        return APPLE_INSIDE_SNAKE
    return block(apple_x,apple_y)

def block_inside_snake(block_x, block_y):
    block_rect = pygame.Rect(block_x, block_y, SQUARE_SIZE, SQUARE_SIZE)
    snake_blocks = my_snake.get_blocks()
    for snake_block in snake_blocks:
        snake_block_rect = pygame.Rect(snake_block.get_pos_x(), snake_block.get_pos_y(), SQUARE_SIZE, SQUARE_SIZE)
        if block_rect.colliderect(snake_block_rect):
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

def distance_between_blocks(block1,block2):
    return abs(block1.get_pos_x()-block2.get_pos_x())+abs(block1.get_pos_y()-block2.get_pos_y())


#drawing functions
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