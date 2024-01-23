import pygame
from snake import snake
from block import block
pygame.init()

SQUARE_SIZE=40
BOARD_LENGTH=15
BOARD_HEIGHT=15
WHITE,BLACK= (98,255,92),(69,232,63)

SNAKE_COLOR=(30,144,255)

gameDisplay = pygame.display.set_mode((1240, 600))
gameDisplay.fill(WHITE)


def main():
    global my_snake
    my_snake=snake()
    while True:
        draw_board()
        my_snake.move()
        draw_snake()
        check_buttons_pressed()
        pygame.display.update()
        pygame.time.delay(10)

def check_buttons_pressed():
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:
            respond_to_button_pressed(event.key)

def opposite_directions(cur_dir,new_dir):
    match cur_dir:
        case "up":
            return new_dir=="down"
        case "down":
            return new_dir == "up"
        case "right":
            return new_dir == "left"
        case "left":
            return new_dir == "right"
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

    if not opposite_directions(cur_dir,new_dir):
        turn_pos_x,turn_pos_y=get_turn_pos(my_snake.get_head_x(),my_snake.get_head_y(),cur_dir,new_dir)
        my_snake.add_turn_pos(turn_pos_x, turn_pos_y, new_dir)

def get_turn_pos(head_x,head_y,cur_dir,turn_dir):
    pos_x,pos_y=0,0
    if turn_dir=="up" or turn_dir=="down":
        pos_y=head_y
        if cur_dir=="left":
            head_x-=SQUARE_SIZE
        else:
            head_x+=SQUARE_SIZE
        pos_x=(head_x//SQUARE_SIZE)*SQUARE_SIZE
    else:
        if cur_dir=="down":
            head_y+=SQUARE_SIZE
        else:
            head_y-=SQUARE_SIZE
        pos_y = (head_y // SQUARE_SIZE) * SQUARE_SIZE
        pos_x = head_x
    return pos_x,pos_y

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
main()