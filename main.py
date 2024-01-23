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
        self.turn_positions=[]
        self.blocks=[block(100,200,"right","head"),block(60,200,"right","normal"), block(20,200,"right","last")]
    def draw_snake(self):
        for block in self.blocks:
            for turn in self.turn_positions:
                if block.get_pos_x()==turn[0] and block.get_pos_y()==turn[1]:
                    block.turn(turn[2])
                    if block.get_type()=="last":
                        self.turn_positions.remove(turn)
                    break
            block.move()
            pygame.draw.rect(gameDisplay, SNAKE_COLOR, [block.get_pos_x(), block.get_pos_y(), SQUARE_SIZE, SQUARE_SIZE])
    def add_turn_pos(self,pos_x,pos_y,dir):
        self.turn_positions.append([pos_x,pos_y,dir])
    def get_head(self):
        return self.blocks[0]
    def turn(self,new_dir):
        self.blocks[0].turn(new_dir)

    def get_head_x(self):
        return self.blocks[0].get_pos_x()
    def get_head_y(self):
        return self.blocks[0].get_pos_y()


def main():
    my_snake=snake()
    while True:
        draw_board()
        snake.draw_snake(my_snake)
        pygame.time.delay(10)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_UP:
                        my_snake.turn("up")
                        my_snake.add_turn_pos(my_snake.get_head_x(),my_snake.get_head_y(),"up")
                    case pygame.K_DOWN:
                        my_snake.turn("down")
                        my_snake.add_turn_pos(my_snake.get_head_x(),my_snake.get_head_y(),"down")
                    case pygame.K_RIGHT:
                        my_snake.turn("right")
                        my_snake.add_turn_pos(my_snake.get_head_x(), my_snake.get_head_y(), "right")
                    case pygame.K_LEFT:
                        my_snake.turn("left")
                        my_snake.add_turn_pos(my_snake.get_head_x(), my_snake.get_head_y(), "left")
        pygame.display.update()













class block:
    def __init__(self,pos_x,pos_y,dir,type):
        self.pos_x=pos_x
        self.pos_y=pos_y
        self.dir=dir
        self.type=type
    def turn(self,new_dir):
        self.dir=new_dir
    def move(self):
        match self.get_direction():
            case "right":
                self.move_right()
            case "left":
                self.move_left()
            case "up":
                self.move_up()
            case "down":
                self.move_down()
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