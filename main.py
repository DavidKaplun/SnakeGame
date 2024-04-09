import sys

import pygame

from board import *
from constants import *
from snake_bot import get_directions_to_apple
import socket
import re
pygame.init()
gameDisplay = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
gameDisplay.fill(WHITE)

font = pygame.font.Font('freesansbold.ttf', FONT_SIZE)
searching_for_players_font=pygame.font.Font('freesansbold.ttf', SEARCHING_FOR_PLAYERS_FONT_SIZE)

username_entry_active = False
password_entry_active = False

username_entry_text = ""
password_entry_text = ""

session_username=""

socket_with_server=""
def try_to_connect_to_server():
    global socket_with_server
    try:
        socket_with_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_with_server.connect((SERVER_IP, SERVER_PORT))
    except Exception as e:
        print(e)

try_to_connect_to_server()

def reset_entries():
    global username_entry_text, password_entry_text, username_entry_active, password_entry_active
    username_entry_text = ""
    password_entry_text = ""

    username_entry_active = False
    password_entry_active = False

def draw_login_page():
    reset_entries()

    global current_screen
    current_screen = "login"
    gameDisplay.fill(WHITE)


    login_text=font.render(LOGIN_TEXT, True, TEXT_COLOR)
    gameDisplay.blit(login_text, (LOGIN_TEXT_OFFSET_X,LOGIN_TEXT_OFFSET_Y))

    username_text = font.render("Username:", True, TEXT_COLOR)
    gameDisplay.blit(username_text, (USERNAME_TEXT_OFFSET_X, USERNAME_TEXT_OFFSET_Y))

    password_text = font.render("Password:", True, TEXT_COLOR)
    gameDisplay.blit(password_text, (PASSWORD_TEXT_OFFSET_X, PASSWORD_TEXT_OFFSET_Y))

    draw_entries()
    pygame.draw.rect(gameDisplay, APPLE_COLOR, LOGIN_BUTTON)
    login_button_text=font.render(LOGIN_TEXT, True, TEXT_COLOR)
    gameDisplay.blit(login_button_text,(LOGIN_BUTTON_OFFSET_X, LOGIN_BUTTON_OFFSET_Y))

    dont_have_account_text=font.render(DONT_HAVE_ACCOUNT_TEXT, True, TEXT_COLOR)
    gameDisplay.blit(dont_have_account_text, (DONT_HAVE_ACCOUNT_TEXT_OFFSET_X, DONT_HAVE_ACCOUNT_TEXT_OFFSET_Y))

def draw_register_page():
    reset_entries()

    global current_screen
    current_screen = "register"
    gameDisplay.fill(WHITE)

    register_text = font.render(REGISTER_TEXT, True, TEXT_COLOR)
    gameDisplay.blit(register_text, (REGISTER_TEXT_OFFSET_X, REGISTER_TEXT_OFFSET_Y))

    username_text = font.render("Username:", True, TEXT_COLOR)
    gameDisplay.blit(username_text, (USERNAME_TEXT_OFFSET_X, USERNAME_TEXT_OFFSET_Y))

    password_text = font.render("Password:", True, TEXT_COLOR)
    gameDisplay.blit(password_text, (PASSWORD_TEXT_OFFSET_X, PASSWORD_TEXT_OFFSET_Y))

    draw_entries()
    pygame.draw.rect(gameDisplay, APPLE_COLOR, REGISTER_BUTTON)
    register_button_text = font.render(REGISTER_TEXT, True, TEXT_COLOR)
    gameDisplay.blit(register_button_text, (REGISTER_BUTTON_OFFSET_X, REGISTER_BUTTON_OFFSET_Y))

    already_have_account_text = font.render(ALREADY_HAVE_ACCOUNT_TEXT, True, TEXT_COLOR)
    gameDisplay.blit(already_have_account_text, (ALREADY_HAVE_ACCOUNT_TEXT_OFFSET_X, ALREADY_HAVE_ACCOUNT_TEXT_OFFSET_Y))

def request_login(username, password):
    response=-1
    try:
        socket_with_server.send(("2 "+username+" "+password).encode())
        response=socket_with_server.recv(1024).decode()
    except Exception as e:
        print(e)

    if response==SUCCESS:
        global session_username
        draw_main_menu()
        session_username=username[:]

    elif response==ERROR:
        error_message=font.render(LOGIN_ERROR_MESSAGE, True, APPLE_COLOR)
        gameDisplay.blit(error_message,(LOGIN_ERROR_MESSAGE_OFFSET_X, LOGIN_ERROR_MESSAGE_OFFSET_Y))
        reset_entries()
        draw_entries()

def request_registration(username, password):
    response = -1
    try:
        socket_with_server.send(("1 " + username + " " + password).encode())
        response = socket_with_server.recv(1024).decode()
        print("response is:",response)
    except Exception as e:
        print(e)
    print("response is:", response)
    if response == SUCCESS:
        global session_username
        draw_main_menu()
        session_username = username[:]

    elif response == ERROR:
        error_message = font.render(REGISTER_ERROR_MESSAGE, True, APPLE_COLOR)
        gameDisplay.blit(error_message, (REGISTER_ERROR_MESSAGE_OFFSET_X, REGISTER_ERROR_MESSAGE_OFFSET_Y))
        reset_entries()
        draw_entries()

def draw_entries():
    draw_entry_rects()
    draw_entry_texts()

def draw_entry_texts():
    username_entry_text_surface = font.render(username_entry_text, True, TEXT_COLOR)
    gameDisplay.blit(username_entry_text_surface, (USERNAME_ENTRY_OFFSET_X, USERNAME_ENTRY_OFFSET_Y))

    password_entry_text_surface = font.render(password_entry_text, True, TEXT_COLOR)
    gameDisplay.blit(password_entry_text_surface, (PASSWORD_ENTRY_OFFSET_X, PASSWORD_ENTRY_OFFSET_Y))

def draw_entry_rects():
    if username_entry_active:
        pygame.draw.rect(gameDisplay, COLOR_ACTIVE, USERNAME_INPUT_RECT)
        pygame.draw.rect(gameDisplay, COLOR_INACTIVE, PASSWORD_INPUT_RECT)
    elif password_entry_active:
        pygame.draw.rect(gameDisplay, COLOR_INACTIVE, USERNAME_INPUT_RECT)
        pygame.draw.rect(gameDisplay, COLOR_ACTIVE, PASSWORD_INPUT_RECT)
    else:
        pygame.draw.rect(gameDisplay, COLOR_INACTIVE, USERNAME_INPUT_RECT)
        pygame.draw.rect(gameDisplay, COLOR_INACTIVE, PASSWORD_INPUT_RECT)



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

    stats_text=get_users_stats().split(" ")[::2]
    print("stats:",stats_text)
    stats_text=["rating:"+stats_text[0],"wins:"+stats_text[1],"loses:"+stats_text[2],"w/l:"+stats_text[3]]

    cur_text_y = FIRST_TEXT_OFFSET
    for line in stats_text:
        txt = font.render(line, True, TEXT_COLOR)
        gameDisplay.blit(txt, (TEXT_OFFSET_X, cur_text_y))
        cur_text_y += TEXT_OFFSET_Y

    draw_back_button()

def get_users_stats():
    response="4"
    try:
        socket_with_server.send(("3 "+session_username).encode())
        while response[-1]!=SEND_STATS:
            response=socket_with_server.recv(BUF_SIZE).decode()
    except Exception as e:
        print(e)
    return response[:-1]

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

    draw_login_page()

    while True:
        pygame.display.update()
        check_buttons_pressed()
        pygame.time.delay(TIME_DELAY)


def multi_player():
    gameDisplay.fill(WHITE)

    searching_for_players_text = font.render("searching for players...", True, TEXT_COLOR)
    gameDisplay.blit(searching_for_players_text, (SEARCHING_FOR_PLAYERS_OFFSET_X, SEARCHING_FOR_PLAYERS_OFFSET_Y))

    pygame.display.update()
    global current_screen
    current_screen = "multi player"

    socket_with_server.send(REQUEST_GAME.encode())
    response = socket_with_server.recv(BUF_SIZE).decode()

    if response == SEARCHING_FOR_PLAYERS:
        print(session_username+" is searching for players")

    response = socket_with_server.recv(BUF_SIZE)#this is not to get a message. this is to wait until the server sends a signal that we can start

    player_board=board(BOARD1_OFFSET_X, BOARD_OFFSET_Y, session_username)
    prev_dir=""
    rival_player_score=0
    rival_player_eating_apple=False
    gameDisplay.fill(WHITE)

    while player_board.snake_is_alive() and player_board.score<WINNING_SCORE:
        player_string_board=convert_board_to_string(player_board)
        is_player_snake_eating_apple=str(player_board.snake_eating_apple())

        socket_with_server.send((SEND_BOARD+"-"+player_string_board+"-"+is_player_snake_eating_apple).encode())
        response=socket_with_server.recv(BUF_SIZE).decode()

        if response[0]==SEND_BOARD:
            message_code,rival_string_board, rival_player_eating_apple=response.split("-")
        else:
            break

        player_board.snake.move()

        if player_board.snake_eating_apple():
            prev_dir = player_board.snake.get_last_block().dir
            player_board.snake.grow()
            update_board(player_board)

            player_board.score+=1

        if rival_player_eating_apple==True:
            rival_player_score+=1
            update_board(player_board)

        draw_board(player_board)
        draw_string_board(rival_string_board)

        draw_player_score(player_board,rival_player_score,"user69")

        pygame.display.update()
        pygame.event.pump()


        last_snake_block=player_board.snake.get_last_block()
        if last_snake_block.dir == "":
            if distance_between_blocks(player_board.snake.blocks[-2], last_snake_block) >= SQUARE_SIZE:
                last_snake_block.turn(prev_dir)


        pygame.time.delay(TIME_DELAY)

    text=""
    if response==LOST_GAME:
        text="you lost game"
    elif response==WON_GAME:
        text="you won game"
    elif player_board.snake_is_alive()==False:
        socket_with_server.send(LOST_GAME.encode())
        text = "you lost game"
    elif player_board.score==WINNING_SCORE:
        socket_with_server.send(WON_GAME.encode())
        text = "you won game"

    pygame.draw.rect(gameDisplay, BACKGROUND_COLOR,[END_OF_GAME_BACKGROUND_X_OFFSET, END_OF_GAME_BACKGROUND_Y_OFFSET, END_OF_GAME_BACKGROUND_LENGTH, END_OF_GAME_BACKGROUND_HEIGHT])

    end_of_game_text = font.render(text, True, TEXT_COLOR)
    gameDisplay.blit(end_of_game_text, (END_OF_GAME_TEXT_OFFSET_X, END_OF_GAME_TEXT_OFFSET_Y))

    draw_end_of_game_buttons()
    current_screen="end of multiplayer game"

def draw_player_score(board,rival_score,rival_name):
    name1 = font.render(session_username, True, TEXT_COLOR)
    gameDisplay.blit(name1, (BOARD1_NAME_OFFSET_X, SCORE_OFFSET_Y))

    score1 = font.render(str(board.score), True, TEXT_COLOR)
    gameDisplay.blit(score1, (BOARD1_SCORE_OFFSET_X, SCORE_OFFSET_Y))

    name2 = font.render(rival_name, True, TEXT_COLOR)
    gameDisplay.blit(name2, (BOARD2_NAME_OFFSET_X, SCORE_OFFSET_Y))

    score2 = font.render(str(rival_score), True, TEXT_COLOR)
    gameDisplay.blit(score2, (BOARD2_SCORE_OFFSET_X, SCORE_OFFSET_Y))

def convert_board_to_string(board):
    board_string = ""
    for block in board.snake.get_blocks():
        board_string += str(block.x) + "," + str(block.y) +"."
    board_string=board_string[:-1]
    board_string += "*"

    if board.wall != INCONSTRACTABLE:
        for block in board.wall:
            board_string += str(block.x) + "," + str(block.y)+"."
        board_string = board_string[:-1]
    else:
        board_string += "."

    board_string += "*"
    board_string += str(board.apple.x) + "," + str(board.apple.y)
    return board_string


def draw_string_board(string_board):
    color = 0
    for y in range(BOARD_HEIGHT):
        for x in range(BOARD_LENGTH):
            if color % 2 == 0:
                pygame.draw.rect(gameDisplay, WHITE,[SQUARE_SIZE * x + BOARD2_OFFSET_X, SQUARE_SIZE * y + BOARD_OFFSET_Y, SQUARE_SIZE, SQUARE_SIZE])
            else:
                pygame.draw.rect(gameDisplay, BLACK,[SQUARE_SIZE * x + BOARD2_OFFSET_X, SQUARE_SIZE * y + BOARD_OFFSET_Y, SQUARE_SIZE, SQUARE_SIZE])
            color += 1

    snake_blocks, wall, apple = string_board.split("*")
    snake_blocks=snake_blocks.split(".")

    for block in snake_blocks:
        block_x, block_y = block.split(",")
        pygame.draw.rect(gameDisplay, SNAKE_COLOR, [int(block_x) + BOARD2_OFFSET_X, int(block_y), SQUARE_SIZE, SQUARE_SIZE])

    if wall != ".":
        wall = wall.split(".")
        for block in wall:
            block_x, block_y = block.split(",")
            pygame.draw.rect(gameDisplay, WALL_COLOR, [int(block_x) + BOARD2_OFFSET_X, int(block_y), SQUARE_SIZE, SQUARE_SIZE])

    apple_x, apple_y = apple.split(",")
    pygame.draw.rect(gameDisplay, APPLE_COLOR, [int(apple_x) + BOARD2_OFFSET_X, int(apple_y), SQUARE_SIZE, SQUARE_SIZE])


def single_player():
    gameDisplay.fill(WHITE)
    global current_screen
    current_screen = "single player"

    human_board=board(BOARD1_OFFSET_X,BOARD_OFFSET_Y, session_username)
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
        check_keyboard_pressed_during_game(human_board)

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

def respond_to_key_pressed(event):
    if current_screen=="login" or current_screen=="register":
        if username_entry_active:
            global username_entry_text
            if event.key==pygame.K_BACKSPACE:#later create a cover for the event that user presses enter
                username_entry_text = username_entry_text[:-1]
            else:
                username_entry_text += event.unicode
        elif password_entry_active:
            global password_entry_text
            if event.key==pygame.K_BACKSPACE:#later create a cover for the event that user presses enter
                password_entry_text = password_entry_text[:-1]
            else:
                password_entry_text += event.unicode

        draw_entries()



def check_keyboard_pressed_during_game(human_board):
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:
            respond_to_key_pressed_during_game(event.key,human_board)


def respond_to_key_pressed_during_game(button_pressed,human_board):
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



def check_buttons_pressed():
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            on_mouse_button_down(event)

        if event.type == pygame.KEYDOWN:
            respond_to_key_pressed(event)

def on_mouse_button_down(event):
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == CLICKED:
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
            if BACK_BUTTON.collidepoint(event.pos):
                draw_main_menu()

        elif current_screen=="end of game":
            if END_OF_GAME_BACK_BUTTON.collidepoint(event.pos):
                draw_main_menu()

            elif PLAY_AGAIN_BUTTON.collidepoint(event.pos):
                single_player()

        elif current_screen=="login":
            respond_if_clicked_on_entries(event)

            if LOGIN_BUTTON.collidepoint(event.pos):
                request_login(username_entry_text, password_entry_text)

            elif DONT_HAVE_ACCOUNT_CLICK_BOX.collidepoint(event.pos):
                draw_register_page()

        elif current_screen=="register":
            respond_if_clicked_on_entries(event)

            if REGISTER_BUTTON.collidepoint(event.pos):
                request_registration(username_entry_text, password_entry_text)

            elif DONT_HAVE_ACCOUNT_CLICK_BOX.collidepoint(event.pos):
                draw_login_page()
        elif current_screen=="end of multiplayer game":
            if END_OF_GAME_BACK_BUTTON.collidepoint(event.pos):
                draw_main_menu()

            elif PLAY_AGAIN_BUTTON.collidepoint(event.pos):
                multi_player()


def respond_if_clicked_on_entries(event):
    global username_entry_active, password_entry_active
    if USERNAME_INPUT_RECT.collidepoint(event.pos):
        username_entry_active = True
        password_entry_active = False
        draw_entries()
    elif PASSWORD_INPUT_RECT.collidepoint(event.pos):
        username_entry_active = False
        password_entry_active = True
        draw_entries()

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