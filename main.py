import sys

from snake import snake
import random
from block import block
from constants import *
from snake_bot import get_directions_to_apple

pygame.init()
gameDisplay = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
gameDisplay.fill(WHITE)

font = pygame.font.Font('freesansbold.ttf', FONT_SIZE)

def draw_main_menu():
    draw_buttons_for_menu()
    draw_texts_for_buttons_in_menu()

def draw_buttons_for_menu():
    pygame.draw.rect(gameDisplay,BUTTON_COLOR,SINGLE_PLAYER_BUTTON)
    pygame.draw.rect(gameDisplay, BUTTON_COLOR, MULTI_PLAYER_BUTTON)
    pygame.draw.rect(gameDisplay, BUTTON_COLOR, MY_STATS_BUTTON)
    pygame.draw.rect(gameDisplay, BUTTON_COLOR, RULES_BUTTON)
    pygame.draw.rect(gameDisplay, BUTTON_COLOR, EXIT_BUTTON)

def draw_texts_for_buttons_in_menu():
    cur_text_y = FIRST_BUTTON_Y_OFFSET + BUTTON_TEXT_Y_OFFSET

    for text in MAIN_MENU_BUTTONS_TEXTS:
        txt = font.render(text, True, (0, 0, 0))
        textRect = txt.get_rect()
        textRect.center=(BUTTONS_X_OFFSET + BUTTON_TEXT_X_OFFSET, cur_text_y)

        gameDisplay.blit(txt, textRect)
        cur_text_y += DISTANCE_BETWEEN_BUTTONS

def draw_background_recktangle():
    pygame.draw.rect(gameDisplay, BACKGROUND_COLOR, (BACKGROUND_OFFSET_X, BACKGROUND_OFFSET_Y,  BACKGROUND_WIDTH, BACKGROUND_HEIGHT))

def draw_rules_screen():
    gameDisplay.fill(WHITE)
    draw_background_recktangle()

    cur_text_y=TEXT_OFFSET_Y+BACKGROUND_OFFSET_Y
    for rule in RULES_TEXT:
        txt = font.render(rule, True, (255, 255, 255))
        cur_text_y+=TEXT_OFFSET_Y
        gameDisplay.blit(txt, (BACKGROUND_OFFSET_X + TEXT_OFFSET_X,  cur_text_y))
        cur_text_y += TEXT_OFFSET_Y

def draw_stats_screen():
    draw_background_recktangle()
    stats_text = "rating:0\nwins:0\nloses:0\nw/l:0%\n"#it will change when I connect the database

    txt = font.render(stats_text, True, (0, 0, 0))
    textRect = txt.get_rect()
    textRect.center(BACKGROUND_OFFSET_X + TEXT_OFFSET_X, BACKGROUND_OFFSET_Y + TEXT_OFFSET_Y)

    gameDisplay.blit(txt, textRect)

def draw_playing_screen():#will implement the functions inside later
    #draw_board_1()
    #draw_board_2()

    #draw_snake_1()
    #draw_snake_2()

    #draw_wall_1()
    #draw_wall_2()

    #draw_apple_1()
    #draw_apple_2()

    #draw_playing_screen_buttons()

    #draw_playing_screen_texts()

    return


def draw_win_screen():
    #draw_win_lose_background()
   # draw_win_text()
    #draw_win_lose_buttons()
    return

def draw_lose_screen():
    #draw_win_lose_background()
    #draw_lose_text()
    #draw_win_lose_buttons()
    return

def draw_win_lose_background():
    return
#
#you will have to create a seprate file for the gui of the game
#

def main():
    draw_main_menu()
    while True:

        pygame.display.update()
        check_buttons_pressed_in_menu()
        pygame.time.delay(TIME_DELAY)

def old_main():
    score=0
    global my_snake,apple
    my_snake=snake()
    apple=create_apple()
    prev_dir=""
    wall = generate_wall()
    my_snake.turn_sequence=get_directions_to_apple(wall,my_snake,apple)
    while snake_is_alive(wall):
        if snake_eating_apple():
            prev_dir = my_snake.get_last_block().dir
            my_snake.grow()
            apple=create_apple()
            wall = generate_wall()
            score+=1
            my_snake.turn_sequence = get_directions_to_apple(wall, my_snake, apple)

        pygame.display.update()
        check_buttons_pressed_in_menu()
        my_snake.move()


        draw_board()
        draw_snake()
        draw_apple()
        draw_wall(wall)

        last_snake_block=my_snake.get_last_block()
        if last_snake_block.dir=="":
            if distance_between_blocks(my_snake.blocks[-2],last_snake_block)>=SQUARE_SIZE:
                last_snake_block.turn(prev_dir)

        pygame.time.delay(TIME_DELAY)
    print("The snake died your score is:",score)

def snake_is_alive(wall):#pass snake here
    snake_head=my_snake.get_head()
    head_rect=pygame.Rect(snake_head.x,snake_head.y,SQUARE_SIZE,SQUARE_SIZE)
    for block in my_snake.get_blocks()[2:]:
        block_rect=pygame.Rect(block.x,block.y,SQUARE_SIZE,SQUARE_SIZE)
        if head_rect.colliderect(block_rect):
            return False
    if outside_board(snake_head) or snake_is_touching_wall(head_rect,wall):
        return False
    return True

def snake_is_touching_wall(head_rect,wall):
    if wall!=INCONSTRACTABLE:
        for block in wall:
            block_rect = pygame.Rect(block.x, block.y, SQUARE_SIZE, SQUARE_SIZE)
            if head_rect.colliderect(block_rect):
                return True
    return False
def snake_eating_apple():#pass snake here
    snake_head=my_snake.get_head()
    apple_rect=pygame.Rect(apple.x,apple.y,SQUARE_SIZE,SQUARE_SIZE)
    snake_head_rect=pygame.Rect(snake_head.x,snake_head.y,SQUARE_SIZE,SQUARE_SIZE)
    return apple_rect.colliderect(snake_head_rect)

def create_apple():#pass snake here
    apple=INVALID_APPLE
    while apple == INVALID_APPLE:
        apple_x=random.randint(0,BOARD_LENGTH-1)*SQUARE_SIZE
        apple_y=random.randint(0,BOARD_HEIGHT-1)*SQUARE_SIZE
        apple=block(apple_x,apple_y)
        if not (block_inside_snake(apple) or distance_between_blocks(apple,my_snake.get_head())<MIN_DIST_BETWEEN_APPLE_AND_SNAKE):
            return apple
        apple = INVALID_APPLE


def block_inside_snake(block):#pass snake here
    block_rect = pygame.Rect(block.x, block.y, SQUARE_SIZE, SQUARE_SIZE)
    snake_blocks = my_snake.get_blocks()
    for snake_block in snake_blocks:
        snake_block_rect = pygame.Rect(snake_block.x, snake_block.y, SQUARE_SIZE, SQUARE_SIZE)
        if block_rect.colliderect(snake_block_rect):
            return True
    return False

def check_buttons_pressed_in_menu():
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:
            respond_to_button_pressed(event.key)

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Call the on_mouse_button_down() function
            on_mouse_button_down(event)

def on_mouse_button_down(event):
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        if SINGLE_PLAYER_BUTTON.collidepoint(event.pos):
            print("single player button pressed")

        if MULTI_PLAYER_BUTTON.collidepoint(event.pos):
            print("multi player button pressed")

        if MY_STATS_BUTTON.collidepoint(event.pos):
            draw_stats_screen()

        if RULES_BUTTON.collidepoint(event.pos):
            draw_rules_screen()

        if EXIT_BUTTON.collidepoint(event.pos):
            pygame.quit()
            sys.exit()

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
    return abs(block1.x-block2.x)+abs(block1.y-block2.y)


#drawing functions
def draw_snake():#pass snake here
    blocks=my_snake.get_blocks()
    for block in blocks:
        pygame.draw.rect(gameDisplay, SNAKE_COLOR, [block.x, block.y, SQUARE_SIZE, SQUARE_SIZE])

def draw_board():#change names
    color = 0
    for y in range(BOARD_HEIGHT):
        for x in range(BOARD_LENGTH):
            if color %2 == 0:
                pygame.draw.rect(gameDisplay, WHITE,[SQUARE_SIZE*x,SQUARE_SIZE*y,SQUARE_SIZE,SQUARE_SIZE])
            else:
                pygame.draw.rect(gameDisplay, BLACK, [SQUARE_SIZE * x, SQUARE_SIZE * y, SQUARE_SIZE, SQUARE_SIZE])
            color += 1

def draw_apple():#pass apple here
    pygame.draw.rect(gameDisplay, APPLE_COLOR, [apple.x, apple.y, SQUARE_SIZE, SQUARE_SIZE])

def draw_wall(wall):
    if wall!=INCONSTRACTABLE:
        for block in wall:
            pygame.draw.rect(gameDisplay, WALL_COLOR, [block.x, block.y, SQUARE_SIZE, SQUARE_SIZE])

#below only the functions related to wall

def chose_wall_type():#pass snake here as well
    snake_head_x,snake_head_y=my_snake.get_head_x(), my_snake.get_head_y()
    difference_x,difference_y=snake_head_x-apple.x, snake_head_y-apple.y
    if abs(difference_x)>abs(difference_y):#if the horizontal distance bigger than vertical then build vertical walls
        if difference_x>0:#because if its possitive then the snake is right from the apple
            return "right"
        return "left"

    else:
        if difference_y>0:#means snake below apple. so build a wall below apple
            return "down"
        return "up"


def chose_start_pos(wall_type):
    if wall_type=="up" or wall_type=="right":
        return block(apple.x + (2*SQUARE_SIZE), apple.y - (2*SQUARE_SIZE))
    return block(apple.x - (2*SQUARE_SIZE), apple.y + (2*SQUARE_SIZE))

def outside_board(block):
    block_x,block_y=block.x,block.y
    return block_x<0 or block_y<0 or block_x>(BOARD_LENGTH-1)*SQUARE_SIZE or block_y>(BOARD_LENGTH-1)*SQUARE_SIZE

def build_wall_blocks(starting_block,build_direction,num_of_blocks_to_build):
    wall=[starting_block]
    cur_point_x, cur_point_y=starting_block.x, starting_block.y

    for i in range(num_of_blocks_to_build):
        option_to_expand = gen_new_block_position_options(cur_point_x, cur_point_y, build_direction)
        new_block = chose(option_to_expand)

        if new_block != INVALID_BLOCK:
            wall.append(new_block)
            cur_point_x, cur_point_y = new_block.x, new_block.y
        else:
            break

    return wall
def generate_wall():
    wall_type=chose_wall_type()

    start_point = chose_start_pos(wall_type)
    if not valid(start_point):
        return INCONSTRACTABLE

    wall=[]
    match wall_type:
        case "up":
            wall=build_wall_blocks(start_point,"left",WALL_LENGTH-1)#the wall_length-1 because we already have 1 block

        case "down":
            wall=build_wall_blocks(start_point,"right",WALL_LENGTH-1)

        case "left":
            wall=build_wall_blocks(start_point,"up",WALL_LENGTH-1)

        case "right":
            wall=build_wall_blocks(start_point,"down",WALL_LENGTH-1)

    if len(wall)<MIN_WALL_LENGTH:
        return INCONSTRACTABLE
    return wall

def chose(pos_options):
    valid_options=[]
    for option in pos_options:
        if valid(option):
            valid_options.append(option)

    num_of_valid_options=len(valid_options)
    if num_of_valid_options==0:
        return INVALID_BLOCK
    return  random.choice(valid_options)

def valid(block):#pass snake here
    return  not block_inside_snake(block) and not block_inside_apple(block) and not outside_board(block)


def block_inside_apple(block):
    return block.x==apple.x and block.y==apple.y

def gen_new_block_position_options(block_x, block_y, build_direction):
    new_block_position_options=[]
    match build_direction:
        case "up":
            for new_x in range(block_x-SQUARE_SIZE,block_x+SQUARE_SIZE,SQUARE_SIZE):
                new_block_position_options.append(block(new_x,block_y-SQUARE_SIZE))

        case "down":
            for new_x in range(block_x-SQUARE_SIZE,block_x+SQUARE_SIZE,SQUARE_SIZE):
                new_block_position_options.append(block(new_x,block_y+SQUARE_SIZE))

        case "right":
            for new_y in range(block_y - SQUARE_SIZE, block_y + SQUARE_SIZE,SQUARE_SIZE):
                new_block_position_options.append(block(block_x+SQUARE_SIZE, new_y))

        case "left":
            for new_y in range(block_y - SQUARE_SIZE, block_y + SQUARE_SIZE,SQUARE_SIZE):
                new_block_position_options.append(block(block_x-SQUARE_SIZE, new_y))

    return new_block_position_options

main()