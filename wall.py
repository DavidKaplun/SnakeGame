import random
from block import block
from constants import SQUARE_SIZE,INVALID_BLOCK

def chose_wall_type(snake_head_block):
    snake_head_x=snake_head_block.get_pos_x()
    snake_head_y=snake_head_block.get_pos_y()
    difference_x,difference_y=snake_head_x-apple_x,snake_head_y-apple_y
    if abs(difference_x)>abs(difference_y):#if the horizontal distance bigger than vertical then build vertical walls
        if difference_x>0:#because if its possitive then the snake is right from the apple
            return "right"
        return "left"

    else:
        if difference_y>0:#means snake below apple. so build a wall below apple
            return "down"
        return "up"

def generate_wall(apple_block,snake_head_block):
    global apple_x,apple_y
    apple_x,apple_y=apple_block.get_pos_x(),apple_block.get_pos_y()
    wall_type=chose_wall_type(snake_head_block)
    wall=[]
    #there should be a function for deciding the starting point based on apple cords
    match wall_type:
        case "up":
            cur_point = block(apple_x + (2*SQUARE_SIZE), apple_y - (2*SQUARE_SIZE))
            cur_point_x, cur_point_y = cur_point.get_pos_x(), cur_point.get_pos_y()
            wall.append(cur_point)
            for z in range(4):#there has to be a constant called wall length
                option_to_expand = gen_new_block_position_options(cur_point_x, cur_point_y, "left")#should get the block not its x and y
                new_block = chose(option_to_expand)
                if new_block!=INVALID_BLOCK:
                    wall.append(new_block)
                    cur_point_x, cur_point_y = new_block.get_pos_x(), new_block.get_pos_y()
                else:
                    break

        case "down":
            cur_point = block(apple_x - (2*SQUARE_SIZE), apple_y + (2*SQUARE_SIZE))
            cur_point_x, cur_point_y = cur_point.get_pos_x(), cur_point.get_pos_y()
            wall.append(cur_point)
            for z in range(4):  # there has to be a constant called wall length
                option_to_expand = gen_new_block_position_options(cur_point_x, cur_point_y,"right")  # should get the block not its x and y
                new_block = chose(option_to_expand)
                if new_block != INVALID_BLOCK:
                    wall.append(new_block)
                    cur_point_x, cur_point_y = new_block.get_pos_x(), new_block.get_pos_y()
                else:
                    break

        case "left":
            cur_point = block(apple_x - (2*SQUARE_SIZE), apple_y + (2*SQUARE_SIZE))
            cur_point_x, cur_point_y = cur_point.get_pos_x(), cur_point.get_pos_y()
            wall.append(cur_point)
            for z in range(4):  # there has to be a constant called wall length
                option_to_expand = gen_new_block_position_options(cur_point_x, cur_point_y, "up")  # should get the block not its x and y
                new_block = chose(option_to_expand)
                if new_block != INVALID_BLOCK:
                    wall.append(new_block)
                    cur_point_x,cur_point_y=new_block.get_pos_x(), new_block.get_pos_y()
                else:
                    break

        case "right":
            cur_point = block(apple_x + (2*SQUARE_SIZE), apple_y - (2*SQUARE_SIZE))
            cur_point_x,cur_point_y=cur_point.get_pos_x(), cur_point.get_pos_y()
            wall.append(cur_point)
            for z in range(4):  # there has to be a constant called wall length
                option_to_expand = gen_new_block_position_options(cur_point_x,cur_point_y,"down")  # should get the block not its x and y
                new_block = chose(option_to_expand)
                if new_block != INVALID_BLOCK:
                    wall.append(new_block)
                    cur_point_x,cur_point_y=new_block.get_pos_x(), new_block.get_pos_y()
                else:
                    break
    return wall

def chose(options):#better name for options
    valid_options=[]
    for option in options:
        if valid(option):
            valid_options.append(option)

    num_of_valid_options=len(valid_options)
    if num_of_valid_options==0:
        return INVALID_BLOCK
    return  random.choice(valid_options)

def valid(pos_option):
    #not block_inside_snake(pos_option.get_pos_x(),pos_option.get_pos_y()) and
    return  not block_inside_apple(pos_option)#fix this later


def block_inside_apple(block):
    return block.get_pos_x()==apple_x and block.get_pos_y()==apple_y

def gen_new_block_position_options(block_x, block_y, build_direction):
    new_block_position_options=[]
    match build_direction:
        case "up":
            for new_x in range(block_x-SQUARE_SIZE,block_x+SQUARE_SIZE,SQUARE_SIZE):
                new_block_position_options.append(block(new_x,block_y-SQUARE_SIZE))

        case "down":
            for new_x in range(block_x-SQUARE_SIZE,block_x+SQUARE_SIZE,SQUARE_SIZE):
                new_block_position_options.append(block(new_x,block_y+SQUARE_SIZE))

        case "right":
            for new_y in range(block_y - SQUARE_SIZE, block_y + SQUARE_SIZE,SQUARE_SIZE):
                new_block_position_options.append(block(block_x+SQUARE_SIZE, new_y))

        case "left":
            for new_y in range(block_y - SQUARE_SIZE, block_y + SQUARE_SIZE,SQUARE_SIZE):
                new_block_position_options.append(block(block_x-SQUARE_SIZE, new_y))

    return new_block_position_options