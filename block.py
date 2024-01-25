SQUARE_SIZE=40
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
