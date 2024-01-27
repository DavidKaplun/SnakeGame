import random
SQUARE_SIZE=40
def chose_wall_type(apple_cords):
    snake_head_x=my_snake.get_head_x()
    snake_head_y=my_snake.get_head_y()
    apple_x,apple_y=apple_cords[0], apple_cords[1]
    difference_x,difference_y=snake_head_x-apple_x,snake_head_y-apple_y
    if abs(difference_x)>abs(difference_y):
        if difference_x>0:
            return "right"
        return "left"

    else:
        if difference_y>0:
            return "down"
        return "up"

def generate_wall(apple_cords):
    wall_type=chose_wall_type(apple_cords)
    wall=[]
    match wall_type:
        case "up":
            first_point = [apple_cords[0] + 2 * SQUARE_SIZE, apple_cords[1] - 2 * SQUARE_SIZE]
            x, y = first_point[0], first_point[1]
            for z in range(4):
                option_to_expand = gen_options(x, y, "left")
                new_block = chose(option_to_expand)
                if valid(new_block):
                    wall.append(new_block)
                    x, y = new_block[0], new_block[1]
                else:
                    break

        case "down":
            first_point = [apple_cords[0] - 2 * SQUARE_SIZE, apple_cords[1] + 2 * SQUARE_SIZE]
            x, y = first_point[0], first_point[1]
            for z in range(4):
                option_to_expand = gen_options(x, y, "right")
                new_block = chose(option_to_expand)
                if valid(new_block):
                    wall.append(new_block)
                    x, y = new_block[0], new_block[1]
                else:
                    break

        case "left":
            first_point=[apple_cords[0]-2*SQUARE_SIZE, apple_cords[1]+2*SQUARE_SIZE]
            x,y=first_point[0],first_point[1]
            for z in range(4):
                option_to_expand=gen_options(x,y,"up")
                new_block=chose(option_to_expand)
                if valid(new_block):
                    wall.append(new_block)
                    x,y=new_block[0],new_block[1]
                else:
                    break

        case "right":
            first_point = [apple_cords[0] + 2 * SQUARE_SIZE, apple_cords[1] - 2 * SQUARE_SIZE]
            x, y = first_point[0], first_point[1]
            for z in range(4):
                option_to_expand = gen_options(x, y, "down")
                new_block = chose(option_to_expand)
                if new_block!=NO_VALID_OPTIONS:
                    wall.append(new_block)
                    x, y = new_block[0], new_block[1]
                else:
                    break
    return wall

def chose(self,options):
    valid_options=[]
    for option in options:
        if self.valid(option):
            valid_options.append(option)
    if len(valid_options)==0:
        return -1
    return  random.choice(valid_options)

def valid(self,option):
    return not block_inside_snake(option[0],option[1]) and not block_inside_apple(option[0],option[1])
def block_inside_snake(block_x, block_y):  # change it to block inside snake
    block_rect = pygame.Rect(block_x, block_y, SQUARE_SIZE, SQUARE_SIZE)
    snake_blocks = my_snake.get_blocks()
    for snake_block in snake_blocks:
        snake_block_rect = pygame.Rect(snake_block.get_pos_x(), snake_block.get_pos_y(), SQUARE_SIZE, SQUARE_SIZE)
        if block_rect.colliderect(snake_block_rect):
            return True
    return False

def block_inside_apple(block_x,block_y,apple_cords):
    return block_x==apple_cords[0] and block_y==apple_cords[1]

def gen_options(block_x, block_y, build_direction):#gen_new_block_position_option
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