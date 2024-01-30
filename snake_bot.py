from constants import *
import copy
def get_directions_to_apple(wall,snake,apple):
    grid=create_grid()
    path=find_shortest_path(grid)
    return convert_path_to_directions(path)

def create_grid(wall,snake,apple):
    grid=[]
    for y in range(BOARD_HEIGHT):
        new_line=[]
        for x in range(BOARD_LENGTH):
            new_line.append(0)
        grid.append(new_line)
    return add(grid,wall,snake,apple)

def add(grid,wall,snake,apple):
    grid[apple.get_pos_y()][apple.get_pos_x()]=APPLE
    if wall!=INCONSTRACTABLE:
        for block in wall:
            grid[block.get_pos_y()][grid.get_pos_x()]=BARRIER
    grid[snake.get_head_y()][snake.get_head_x()]=SNAKE_HEAD
    for block in snake.get_blocks()[1:]:
        grid[block.get_pos_y()][block.get_pos_x()]=BARRIER
    return grid

def convert_path_to_directions(path):
    directions=[]
    cur_block = path[0]
    for block in path[1:]:
        directions.append(decide_turn_dir(cur_block,block))
        cur_block=copy.copy(block)
    return directions


def decide_turn_dir(block1,block2):
    difference_x=block1.get_pos_x()-block2.get_pos_x()
    difference_y=block1.get_pos_y()-block2.get_pos_y()

    if difference_x>0:
        return "left"
    elif difference_x<0:
        return "right"
    elif difference_y>0:
        return "up"
    return "down"
