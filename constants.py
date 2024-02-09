#sizes
SQUARE_SIZE=40
BOARD_LENGTH=15
BOARD_HEIGHT=15
SCREEN_WIDTH=1240
SCREEN_HEIGHT=600

#colors
WHITE,BLACK= (98,255,92),(69,232,63)
SNAKE_COLOR=(30,144,255)
APPLE_COLOR=(255,0,0)
WALL_COLOR=(101,53,15)

#wall types
HORIZONTAL=1
VERTICAL=2

#snake speed
SPEED=2

#time
TIME_DELAY=10

#index
FIRST=0
LAST=-1

INVALID_BLOCK=-1
INVALID_APPLE=-1
INCONSTRACTABLE=-1

MIN_DIST_BETWEEN_APPLE_AND_SNAKE=8*SQUARE_SIZE

#wall length constants
MIN_WALL_LENGTH=3
WALL_LENGTH=5

#grid representation constants
EMPTY=0
SNAKE_HEAD=1
APPLE=2
BARRIER=3
BLOCK_TO_MOVE_TO=4


#main menu constants
FIRST_BUTTON_Y_OFFSET=3*SQUARE_SIZE
BUTTONS_X_OFFSET=15*SQUARE_SIZE

BUTTONS_LENGTH=6*SQUARE_SIZE
BUTTONS_HEIGHT=2*SQUARE_SIZE

DISTANCE_BETWEEN_BUTTONS=SQUARE_SIZE

NUM_OF_BUTTONS=5

BUTTON_COLOR=(255,0,0)

MAIN_MENU_BUTTONS_TEXTS=["Single Player","Multiplayer","My Stats","Rules","Exit"]

BUTTON_TEXT_Y_OFFSET=5
BUTTON_TEXT_X_OFFSET=2*SQUARE_SIZE


FONT_SIZE=60



#rules and stats constants
BACKGROUND_OFFSET_X = 15 * SQUARE_SIZE
BACKGROUND_OFFSET_Y = 4 * SQUARE_SIZE

BACKGROUND_HEIGHT = 15 * SQUARE_SIZE
BACKGROUND_WIDTH = 6 * SQUARE_SIZE

RULES_TEXT="1.board is 15x15\n2.screen size of game is 31x15\n3.snake starts 3 blocks long\n4.1 apple = 1 point (for every point a snake gets 1 block longer)\n5.when 1 of the players eats an apple then the apple reappears in a different place on BOTH players boards\n6.every time a new apple appears, so is a wall of 3-5 blocks\nbetween the snake and the apple itself\n7.if a players hits a wall or himself then he loses,\nregardless of how many points he has\n8.first one to get to score 30, wins"

TEXT_OFFSET_X=20
TEXT_OFFSET_Y=10