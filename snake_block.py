from block import block
from constants import SPEED
class snake_block(block):
    def __init__(self,pos_x,pos_y,dir,type):
        block.__init__(self,pos_x,pos_y)
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
    def get_direction(self):
        return self.dir
    def get_type(self):
        return self.type

    def move_up(self):
        self.pos_y-=SPEED
    def move_down(self):
        self.pos_y+=SPEED
    def move_right(self):
        self.pos_x+=SPEED
    def move_left(self):
        self.pos_x-=SPEED
