from block import *
from copy import copy
class snake:
    def __init__(self):
        self.turn_sequence=[]
        self.turn_positions=[]
        self.blocks=[block(100,200,"right","head"),block(60,200,"right","normal"), block(20,200,"right","last")]
    def get_blocks(self):
        return self.blocks

    def grow(self):
        new_block=copy(self.blocks[-1])
        self.blocks[-1].type="normal"
        new_block.dir=""
        self.blocks.append(new_block)

    def move(self):
        for cur_turn in self.turn_sequence:
            cur_head_x=self.get_head_x()
            cur_head_y=self.get_head_y()
            if cur_head_x%SQUARE_SIZE==0 and cur_head_y%SQUARE_SIZE==0:
                new_dir = self.turn_sequence.pop(0)
                if not opposite_directions(self.get_direction(),new_dir):
                    self.turn(new_dir)
                    self.turn_positions.append([cur_head_x,cur_head_y,new_dir])#fix this shit later
                    break

        for block in self.blocks:
            for turn in self.turn_positions:
                if block.get_pos_x()==turn[0] and block.get_pos_y()==turn[1]:
                    block.turn(turn[2])
                    if block.get_type()=="last":
                        self.turn_positions.pop(0)
                    break
            block.move()
    def add_turn_pos(self,pos_x,pos_y,dir):
        self.turn_positions.append([pos_x,pos_y,dir])
    def add_turn(self,direction):
        self.turn_sequence.append(direction)
    def get_head(self):
        return self.blocks[0]
    def turn(self,new_dir):
        self.blocks[0].turn(new_dir)

    def get_head_x(self):
        return self.blocks[0].get_pos_x()
    def get_head_y(self):
        return self.blocks[0].get_pos_y()
    def get_direction(self):
        return self.blocks[0].get_direction()

def distance_between_blocks(block1,block2):
    return abs(block1.get_pos_x()-block2.get_pos_x())+abs(block1.get_pos_y()-block2.get_pos_y())

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