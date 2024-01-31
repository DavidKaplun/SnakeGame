from snake_block import snake_block
from copy import copy
from constants import SQUARE_SIZE,FIRST,LAST
class snake:
    def __init__(self):
        self.turn_sequence=[]
        self.turn_positions=[]
        self.blocks=[snake_block(100,200,"right","head"),snake_block(60,200,"right","normal"), snake_block(20,200,"right","last")]
    def get_blocks(self):
        return self.blocks

    def grow(self):
        new_block=copy(self.get_last_block())
        self.get_last_block().type="normal"
        new_block.dir=""
        self.blocks.append(new_block)

    def move(self):
        for cur_turn in self.turn_sequence:
            cur_head_x=self.get_head_x()
            cur_head_y=self.get_head_y()
            if cur_head_x%SQUARE_SIZE==0 and cur_head_y%SQUARE_SIZE==0:
                new_dir = self.turn_sequence.pop(FIRST)
                if not opposite_directions(self.get_direction(),new_dir):
                    self.turn(new_dir)
                    self.turn_positions.append([cur_head_x,cur_head_y,new_dir])
                    break

        for block in self.blocks:
            for turn in self.turn_positions:
                if block.x==turn[0] and block.y==turn[1]:#there has to be turn x and turn y instead
                    block.turn(turn[2])
                    if block.type=="last":
                        self.turn_positions.pop(FIRST)
                    break
            block.move()
    def add_turn_pos(self,pos_x,pos_y,dir):
        self.turn_positions.append([pos_x,pos_y,dir])
    def add_turn(self,direction):
        self.turn_sequence.append(direction)

    def turn(self,new_dir):
        self.blocks[FIRST].turn(new_dir)


    def get_head(self):
        return self.blocks[FIRST]
    def get_last_block(self):
        return self.blocks[LAST]

    def get_head_x(self):
        return self.blocks[FIRST].x
    def get_head_y(self):
        return self.blocks[FIRST].y
    def get_direction(self):
        return self.blocks[FIRST].dir



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