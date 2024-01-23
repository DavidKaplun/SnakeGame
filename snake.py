from block import block
class snake:
    def __init__(self):
        self.turn_positions=[]
        self.blocks=[block(100,200,"right","head"),block(60,200,"right","normal"), block(20,200,"right","last")]
    def get_blocks(self):
        return self.blocks

    def move(self):
        for block in self.blocks:
            for turn in self.turn_positions:
                if block.get_pos_x()==turn[0] and block.get_pos_y()==turn[1]:
                    block.turn(turn[2])
                    if block.get_type()=="last":
                        self.turn_positions.remove(turn)
                    break
            block.move()
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
    def get_direction(self):
        return self.blocks[0].get_direction()

