class block:
    def __init__(self,pos_x,pos_y):
        self.set_pos_x(pos_x)
        self.set_pos_y(pos_y)
    def get_pos_x(self):
        return self.pos_x
    def get_pos_y(self):
        return self.pos_y
    def set_pos_x(self,pos_x):
        self.pos_x=pos_x

    def set_pos_y(self,pos_y):
        self.pos_y=pos_y