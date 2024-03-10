import sys
from board import *
from constants import *
from snake_bot import get_directions_to_apple
import socket
pygame.init()
gameDisplay = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
gameDisplay.fill(WHITE)

font = pygame.font.Font('freesansbold.ttf', FONT_SIZE)


def multi_player():
    gameDisplay.fill(WHITE)
    global current_screen
    current_screen = "multi player"

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_IP, SERVER_PORT))
    client_socket.send("Hello world!".encode())
    print(client_socket.recv(1024).decode())
    client_socket.close()
def draw_main_menu():
    gameDisplay.fill(WHITE)
    global current_screen
    current_screen="main menu"

    draw_buttons_for_menu()
    draw_texts_for_buttons_in_menu()

def draw_rules_screen():
    gameDisplay.fill(WHITE)
    draw_background_recktangle()

    global current_screen
    current_screen= "rules"

    title=font.render(RULES_TITLE_TEXT,True, TEXT_COLOR)
    gameDisplay.blit(title,(TITLE_X_OFFSET,TITLE_Y_OFFSET))

    cur_text_y=FIRST_TEXT_OFFSET+BACKGROUND_OFFSET_Y
    for line in RULES_TEXT:
        txt = font.render(line, True, TEXT_COLOR)
        gameDisplay.blit(txt, (TEXT_OFFSET_X,  cur_text_y))
        cur_text_y += TEXT_OFFSET_Y

    draw_back_button()
def draw_stats_screen():
    gameDisplay.fill(WHITE)
    draw_background_recktangle()

    title = font.render(STATS_TITLE_TEXT, True, TEXT_COLOR)
    gameDisplay.blit(title, (TITLE_X_OFFSET, TITLE_Y_OFFSET))

    global current_screen
    current_screen = "stats"
    stats_text = ["rating:0","wins:0","loses:0","w/l:0%"]  # it will change when I connect the database

    cur_text_y = FIRST_TEXT_OFFSET
    for line in stats_text:
        txt = font.render(line, True, TEXT_COLOR)
        gameDisplay.blit(txt, (TEXT_OFFSET_X, cur_text_y))
        cur_text_y += TEXT_OFFSET_Y

    draw_back_button()



def draw_back_button():
    pygame.draw.rect(gameDisplay,BUTTON_COLOR,BACK_BUTTON)
    txt = font.render(BACK_BUTTON_TEXT, True, TEXT_COLOR)
    gameDisplay.blit(txt,(BACK_BUTTON_TEXT_X_OFFSET,BACK_BUTTON_TEXT_Y_OFFSET))


def draw_buttons_for_menu():
    pygame.draw.rect(gameDisplay,BUTTON_COLOR,SINGLE_PLAYER_BUTTON)
    pygame.draw.rect(gameDisplay, BUTTON_COLOR, MULTI_PLAYER_BUTTON)
    pygame.draw.rect(gameDisplay, BUTTON_COLOR, MY_STATS_BUTTON)
    pygame.draw.rect(gameDisplay, BUTTON_COLOR, RULES_BUTTON)
    pygame.draw.rect(gameDisplay, BUTTON_COLOR, EXIT_BUTTON)


def draw_texts_for_buttons_in_menu():
    cur_text_y = FIRST_BUTTON_Y_OFFSET + BUTTON_TEXT_Y_OFFSET

    for text in MAIN_MENU_BUTTONS_TEXTS:
        txt = font.render(text, True, TEXT_COLOR)
        textRect = txt.get_rect()
        textRect.center=(BUTTONS_X_OFFSET + BUTTON_TEXT_X_OFFSET, cur_text_y)

        gameDisplay.blit(txt, textRect)
        cur_text_y += DISTANCE_BETWEEN_BUTTONS

def draw_background_recktangle():
    pygame.draw.rect(gameDisplay, BACKGROUND_COLOR, (BACKGROUND_OFFSET_X, BACKGROUND_OFFSET_Y,  BACKGROUND_WIDTH, BACKGROUND_HEIGHT))

def main():
    global current_screen
    current_screen="main menu"
    draw_main_menu()

    while True:
        pygame.display.update()
        check_buttons_pressed()
        pygame.time.delay(TIME_DELAY)


def single_player():
    gameDisplay.fill(WHITE)
    global current_screen
    current_screen = "single player"

    human_board=board(BOARD1_OFFSET_X,BOARD_OFFSET_Y,"human")
    bot_board=board(BOARD2_OFFSET_X, BOARD_OFFSET_Y,"bot")
    draw_scores(human_board, bot_board)
    prev_dir1, prev_dir2="",""
    bot_board.snake.turn_sequence=get_directions_to_apple(bot_board.wall, bot_board.snake, bot_board.apple)
    while human_board.snake_is_alive() and bot_board.snake_is_alive():
        human_board.snake.move()
        bot_board.snake.move()

        if human_board.snake_eating_apple():
            prev_dir1 = human_board.snake.get_last_block().dir
            human_board.snake.grow()

            update_board(human_board)
            update_board(bot_board)

            bot_board.snake.turn_sequence=get_directions_to_apple(bot_board.wall, bot_board.snake, bot_board.apple)

            human_board.score += 1
            gameDisplay.fill(WHITE)
            draw_scores(human_board, bot_board)

        if bot_board.snake_eating_apple():
            prev_dir2 = bot_board.snake.get_last_block().dir
            bot_board.snake.grow()

            update_board(human_board)
            update_board(bot_board)

            bot_board.snake.turn_sequence = get_directions_to_apple(bot_board.wall, bot_board.snake, bot_board.apple)

            bot_board.score += 1
            gameDisplay.fill(WHITE)
            draw_scores(human_board,bot_board)

        draw_board(human_board)
        draw_board(bot_board)
        pygame.display.update()
        check_keyboard_pressed(human_board)

        draw_board(human_board)
        draw_board(bot_board)

        last_snake1_block = human_board.snake.get_last_block()
        last_snake2_block = bot_board.snake.get_last_block()

        if last_snake1_block.dir == "":
            if distance_between_blocks(human_board.snake.blocks[-2], last_snake1_block) >= SQUARE_SIZE:
                last_snake1_block.turn(prev_dir1)

        if last_snake2_block.dir == "":
            if distance_between_blocks(bot_board.snake.blocks[-2], last_snake2_block) >= SQUARE_SIZE:
                last_snake2_block.turn(prev_dir2)
        pygame.time.delay(TIME_DELAY)

    print("scores:",human_board.score,bot_board.score)
    current_screen = "end of game"
    draw_end_of_game_screen(human_board, bot_board)

def draw_end_of_game_screen(human_board,bot_board):
    pygame.draw.rect(gameDisplay,BACKGROUND_COLOR,[END_OF_GAME_BACKGROUND_X_OFFSET, END_OF_GAME_BACKGROUND_Y_OFFSET, END_OF_GAME_BACKGROUND_LENGTH, END_OF_GAME_BACKGROUND_HEIGHT])
    text = "You "

    if human_board.snake_is_alive() and bot_board.snake_is_alive():
        if human_board.score<bot_board.score:
            text += "lost"
        else:
            "won"
    elif human_board.snake_is_alive():
        text += "won"
    else:
        text += "lost"

    end_of_game_text = font.render(text, True, TEXT_COLOR)
    gameDisplay.blit(end_of_game_text, (END_OF_GAME_TEXT_OFFSET_X, END_OF_GAME_TEXT_OFFSET_Y))

    draw_end_of_game_buttons()

def draw_end_of_game_buttons():
    pygame.draw.rect(gameDisplay,BUTTON_COLOR,END_OF_GAME_BACK_BUTTON)

    end_of_game_back_button_text = font.render(BACK_BUTTON_TEXT, True, TEXT_COLOR)
    gameDisplay.blit(end_of_game_back_button_text, (END_OF_GAME_BACK_BUTTON_TEXT_X_OFFSET, END_OF_GAME_BACK_BUTTON_TEXT_Y_OFFSET))

    pygame.draw.rect(gameDisplay, BUTTON_COLOR, PLAY_AGAIN_BUTTON)
    play_again_button_text = font.render("Play Again", True, TEXT_COLOR)
    gameDisplay.blit(play_again_button_text ,(PLAY_AGAIN_BUTTON_TEXT_X_OFFSET, PLAY_AGAIN_BUTTON_TEXT_Y_OFFSET))

def draw_scores(board1,board2):
    name1 = font.render(board1.name, True, TEXT_COLOR)
    gameDisplay.blit(name1, (BOARD1_NAME_OFFSET_X, SCORE_OFFSET_Y))

    score1 = font.render(str(board1.score), True, TEXT_COLOR)
    gameDisplay.blit(score1, (BOARD1_SCORE_OFFSET_X, SCORE_OFFSET_Y))

    name2 = font.render(board2.name, True, TEXT_COLOR)
    gameDisplay.blit(name2, (BOARD2_NAME_OFFSET_X, SCORE_OFFSET_Y))

    score2 = font.render(str(board2.score), True, TEXT_COLOR)
    gameDisplay.blit(score2, (BOARD2_SCORE_OFFSET_X, SCORE_OFFSET_Y))

def update_board(board):
    board.apple=board.create_apple()
    board.wall=board.generate_wall()

def check_buttons_pressed():
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Call the on_mouse_button_down() function
            on_mouse_button_down(event)

def check_keyboard_pressed(human_board):
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:
            respond_to_key_pressed(event.key,human_board)

def on_mouse_button_down(event):
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        if current_screen=="main menu":
            if SINGLE_PLAYER_BUTTON.collidepoint(event.pos):
                single_player()

            if MULTI_PLAYER_BUTTON.collidepoint(event.pos):
                multi_player()

            if MY_STATS_BUTTON.collidepoint(event.pos):
                draw_stats_screen()

            if RULES_BUTTON.collidepoint(event.pos):
                draw_rules_screen()

            if EXIT_BUTTON.collidepoint(event.pos):
                pygame.quit()
                sys.exit()

        elif current_screen=="rules" or current_screen=="stats":
            if BACK_BUTTON.collidepoint((event.pos)):
                draw_main_menu()

        elif current_screen=="end of game":
            if END_OF_GAME_BACK_BUTTON.collidepoint(event.pos):
                draw_main_menu()

            elif PLAY_AGAIN_BUTTON.collidepoint(event.pos):
                single_player()



def respond_to_key_pressed(button_pressed,human_board):
    cur_dir = human_board.snake.get_direction()
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

    human_board.snake.add_turn(new_dir)

def distance_between_blocks(block1,block2):
    return abs(block1.x-block2.x)+abs(block1.y-block2.y)


#drawing functions
def draw_snake(snake):
    blocks=snake.get_blocks()
    for block in blocks:
        pygame.draw.rect(gameDisplay, SNAKE_COLOR, [block.x, block.y, SQUARE_SIZE, SQUARE_SIZE])

def draw_board(board):#change names
    color = 0
    for y in range(BOARD_HEIGHT):
        for x in range(BOARD_LENGTH):
            if color %2 == 0:
                pygame.draw.rect(gameDisplay, WHITE,[SQUARE_SIZE*x+board.offset_x, SQUARE_SIZE*y+board.offset_y, SQUARE_SIZE,SQUARE_SIZE])
            else:
                pygame.draw.rect(gameDisplay, BLACK, [SQUARE_SIZE * x + board.offset_x, SQUARE_SIZE * y + board.offset_y, SQUARE_SIZE, SQUARE_SIZE])
            color += 1
    draw_snake(board.snake)
    draw_apple(board.apple)
    draw_wall(board.wall)

def draw_apple(apple):
    pygame.draw.rect(gameDisplay, APPLE_COLOR, [apple.x, apple.y, SQUARE_SIZE, SQUARE_SIZE])

def draw_wall(wall):
    if wall!=INCONSTRACTABLE:
        for block in wall:
            pygame.draw.rect(gameDisplay, WALL_COLOR, [block.x, block.y, SQUARE_SIZE, SQUARE_SIZE])

#below only the functions related to wall

main()