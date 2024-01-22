import pygame
pygame.init()

SQUARE_SIZE=40
BOARD_LENGTH=15
BOARD_HEIGHT=15
WHITE,BLACK= (98,255,92),(69,232,63)

SNAKE_COLOR=(30,144,255)

gameDisplay = pygame.display.set_mode((1240, 600))
gameDisplay.fill(WHITE)


class snake:
    def __init__(self):
        self.blocks=[head,block1, block2]
    def draw_snake(self):
        for block in self.blocks:

class block:
    def __init__(self,pos_x,pos_y,dir,type):
        self.pos_x=pos_x
        self.pos_y=pos_y
        self.dir=dir
        self.type=type
    def get_pos_x(self):
        return self.pos_x
    def get_pos_y(self):
        return self.pos_y
    def get_direction(self):
        return self.dir
    def get_type(self):
        return self.type

    def move_up(self):
        self.pos_y-=2
    def move_down(self):
        self.pos_y+=2
    def move_right(self):
        self.pos_x+=2
    def move_left(self):
        self.pos_x-=2

def draw_snake(x):
    pygame.draw.rect(gameDisplay, SNAKE_COLOR, [x, 200, SQUARE_SIZE, SQUARE_SIZE])
    pygame.draw.rect(gameDisplay, SNAKE_COLOR, [x+SQUARE_SIZE, 200, SQUARE_SIZE, SQUARE_SIZE])
    pygame.draw.rect(gameDisplay, SNAKE_COLOR, [x+SQUARE_SIZE*2, 200, SQUARE_SIZE, SQUARE_SIZE])


def main():
    x = 100
    while True:
        draw_board()
        draw_snake(x)
        x += 1
        pygame.time.delay(10)
        pygame.display.update()
















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