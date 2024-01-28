import random
SQUARE_SIZE=40
INVALID_BLOCK=-1
def chose_wall_type(apple_block,snake_head_block):#should get apple block and snake head block
    snake_head_x=my_snake.get_head_x()
    snake_head_y=my_snake.get_head_y()
    apple_x,apple_y=apple_cords[0], apple_cords[1]#should be apple get x, apple get y
    difference_x,difference_y=snake_head_x-apple_x,snake_head_y-apple_y
    if abs(difference_x)>abs(difference_y):#if the horizontal distance bigger than vertical then build vertical walls
        if difference_x>0:#because if its possitive then the snake is right from the apple
            return "right"
        return "left"

    else:
        if difference_y>0:
            return "down"
        return "up"

def generate_wall(apple_cords):
    apple_x,apple_y=apple_cords[0],apple_cords[1]#should be apple get x, apple get y
    wall_type=chose_wall_type(apple_cords)#maybe send the x and y of the apple which you already have, to this function
    wall=[]
    #there should be a function for deciding the starting point based on apple cords
    match wall_type:
        case "up":
            first_point = [apple_x + 2 * SQUARE_SIZE, apple_y - 2 * SQUARE_SIZE]#those are the values you give to cur_point
            cur_point_x, cur_point_y = first_point[0], first_point[1]#should be new block called cur_point there should be an append of this point too
            for z in range(4):#there has to be a constant called wall length
                option_to_expand = gen_new_block_position_options(cur_point_x, cur_point_y, "left")#should get the block not its x and y
                new_block = chose(option_to_expand)
                if new_block!=INVALID_BLOCK:
                    wall.append(new_block)
                    cur_point_x, cur_point_y = new_block[0], new_block[1]#this should be removed
                else:
                    break

        case "down":
            first_point = [apple_cords[0] - 2 * SQUARE_SIZE, apple_cords[1] + 2 * SQUARE_SIZE]#those are the values you give to cur_point
            cur_point_x, cur_point_y = first_point[0], first_point[1]#should be new block called cur_point there should be an append of this point too
            for z in range(4):#there has to be a constant called wall length
                option_to_expand = gen_new_block_position_options(cur_point_x, cur_point_y, "right")#should get the block not its x and y
                new_block = chose(option_to_expand)
                if new_block!=INVALID_BLOCK:
                    wall.append(new_block)
                    cur_point_x, cur_point_y = new_block[0], new_block[1]#this should be removed
                else:
                    break

        case "left":
            first_point=[apple_cords[0]-2*SQUARE_SIZE, apple_cords[1]+2*SQUARE_SIZE]#those are the values you give to cur_point
            cur_point_x, cur_point_y=first_point[0],first_point[1]#should be new block called cur_point there should be an append of this point too
            for z in range(4):#there has to be a constant called wall length
                option_to_expand=gen_new_block_position_options(cur_point_x, cur_point_y,"up")#should get the block not its x and y
                new_block=chose(option_to_expand)
                if new_block!=INVALID_BLOCK:
                    wall.append(new_block)
                    cur_point_x, cur_point_y=new_block[0],new_block[1]#this should be removed
                else:
                    break

        case "right":
            first_point = [apple_cords[0] + 2 * SQUARE_SIZE, apple_cords[1] - 2 * SQUARE_SIZE]#those are the values you give to cur_point
            cur_point_x, cur_point_y = first_point[0], first_point[1]#should be new block called cur_point there should be an append of this point too
            for z in range(4):#there has to be a constant called wall length
                option_to_expand = gen_new_block_position_options(cur_point_x, cur_point_y, "down")#should get the block not its x and y
                new_block = chose(option_to_expand)
                if new_block!=INVALID_BLOCK:
                    wall.append(new_block)
                    cur_point_x, cur_point_y = new_block[0], new_block[1]#this should be removed
                else:
                    break
    return wall

def chose(options):
    valid_options=[]#should be list of blocks
    for option in options:
        if valid(option):
            valid_options.append(option)

    num_of_valid_options=len(valid_options)
    if num_of_valid_options==0:#should make this more clear that there are no options
        return INVALID_BLOCK
    return  random.choice(valid_options)

def valid(self,option):
    return not block_inside_snake(option[0],option[1]) and not block_inside_apple(option[0],option[1])
def block_inside_snake(block_x, block_y):  # change it to block_rect instaed of x,y
    block_rect = pygame.Rect(block_x, block_y, SQUARE_SIZE, SQUARE_SIZE)
    snake_blocks = my_snake.get_blocks()
    for snake_block in snake_blocks:
        snake_block_rect = pygame.Rect(snake_block.get_pos_x(), snake_block.get_pos_y(), SQUARE_SIZE, SQUARE_SIZE)#should be a getter to the already created pygame rectangle
        if block_rect.colliderect(snake_block_rect):
            return True
    return False

def block_inside_apple(block_x,block_y,apple_cords):#should be block rect and apple rect
    return block_x==apple_cords[0] and block_y==apple_cords[1]

def gen_new_block_position_options(block_x, block_y, build_direction):#gen_new_block_position_options
    new_block_position_options=[]
    match build_direction:
        case "up":
            for new_x in range(block_x-SQUARE_SIZE,block_x+SQUARE_SIZE):
                new_block_position_options.append((new_x,block_y-1))

        case "down":
            for new_x in range(block_x-SQUARE_SIZE,block_x+SQUARE_SIZE):
                new_block_position_options.append((new_x,block_y+1))

        case "right":
            for new_y in range(block_y - SQUARE_SIZE, block_y + SQUARE_SIZE):
                new_block_position_options.append((block_x+1, new_y))

        case "left":
            for new_y in range(block_y - SQUARE_SIZE, block_y + SQUARE_SIZE):
                new_block_position_options.append((block_x-1, new_y))

    return new_block_position_options