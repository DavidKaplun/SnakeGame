from snake import snake
from constants import *
import random
from block import block
import pygame

class board:

    def __init__(self,board_offset_x,board_offset_y):
        self.offset_x = board_offset_x
        self.offset_y = board_offset_y
        self.snake=snake(board_offset_x,board_offset_y)
        self.apple=self.create_apple()
        self.wall=self.generate_wall()
        self.score=0

    def create_apple(self):
        apple = INVALID_APPLE
        while apple == INVALID_APPLE:
            apple_x = random.randint(0, BOARD_LENGTH - 1) * SQUARE_SIZE + self.offset_x
            apple_y = random.randint(0, BOARD_HEIGHT - 1) * SQUARE_SIZE + self.offset_y
            apple = block(apple_x, apple_y)
            if not (self.block_inside_snake(apple) or distance_between_blocks(apple, self.snake.get_head()) < MIN_DIST_BETWEEN_APPLE_AND_SNAKE):
                return apple
            apple = INVALID_APPLE

    def block_inside_apple(self, block):
        return block.x == self.apple.x and block.y == self.apple.y

    def generate_wall(self):
        wall_type = self.chose_wall_type()

        start_point = self.chose_start_pos(wall_type)
        if not self.valid(start_point):
            return INCONSTRACTABLE

        wall = []
        match wall_type:
            case "up":
                wall = self.build_wall_blocks(start_point, "left", WALL_LENGTH - 1)  # the wall_length-1 because we already have 1 block

            case "down":
                wall = self.build_wall_blocks(start_point, "right", WALL_LENGTH - 1)

            case "left":
                wall = self.build_wall_blocks(start_point, "up", WALL_LENGTH - 1)

            case "right":
                wall = self.build_wall_blocks(start_point, "down", WALL_LENGTH - 1)

        if len(wall) < MIN_WALL_LENGTH:
            return INCONSTRACTABLE
        return wall

    def chose_wall_type(self):  # pass snake here as well
        snake_head_x, snake_head_y = self.snake.get_head_x(), self.snake.get_head_y()
        difference_x, difference_y = snake_head_x - self.apple.x, snake_head_y - self.apple.y
        if abs(difference_x) > abs(difference_y):  # if the horizontal distance bigger than vertical then build vertical walls
            if difference_x > 0:  # because if its possitive then the snake is right from the apple
                return "right"
            return "left"

        else:
            if difference_y > 0:  # means snake below apple. so build a wall below apple
                return "down"
            return "up"

    def chose_start_pos(self,wall_type):
        if wall_type == "up" or wall_type == "right":
            return block(self.apple.x + (2 * SQUARE_SIZE), self.apple.y - (2 * SQUARE_SIZE))
        return block(self.apple.x - (2 * SQUARE_SIZE), self.apple.y + (2 * SQUARE_SIZE))

    def build_wall_blocks(self,starting_block, build_direction, num_of_blocks_to_build):
        wall = [starting_block]
        cur_point_x, cur_point_y = starting_block.x, starting_block.y

        for i in range(num_of_blocks_to_build):
            option_to_expand = gen_new_block_position_options(cur_point_x, cur_point_y, build_direction)
            new_block = self.chose(option_to_expand)

            if new_block != INVALID_BLOCK:
                wall.append(new_block)
                cur_point_x, cur_point_y = new_block.x, new_block.y
            else:
                break

        return wall

    def chose(self,pos_options):
        valid_options = []
        for option in pos_options:
            if self.valid(option):
                valid_options.append(option)

        num_of_valid_options = len(valid_options)
        if num_of_valid_options == 0:
            return INVALID_BLOCK
        return random.choice(valid_options)


    def valid(self,block):
        return not self.block_inside_snake(block) and not self.block_inside_apple(block) and not self.outside_board(block)

    def snake_is_alive(self):
        snake_head = self.snake.get_head()
        head_rect = pygame.Rect(snake_head.x, snake_head.y, SQUARE_SIZE, SQUARE_SIZE)
        for block in self.snake.get_blocks()[2:]:
            block_rect = pygame.Rect(block.x, block.y, SQUARE_SIZE, SQUARE_SIZE)
            if head_rect.colliderect(block_rect):
                return False
        if self.outside_board(snake_head) or self.snake_is_touching_wall(head_rect):
            return False
        return True

    def snake_is_touching_wall(self,head_rect):
        if self.wall != INCONSTRACTABLE:
            for block in self.wall:
                block_rect = pygame.Rect(block.x, block.y, SQUARE_SIZE, SQUARE_SIZE)
                if head_rect.colliderect(block_rect):
                    return True
        return False

    def block_inside_snake(self,block):
        block_rect = pygame.Rect(block.x, block.y, SQUARE_SIZE, SQUARE_SIZE)
        snake_blocks = self.snake.get_blocks()
        for snake_block in snake_blocks:
            snake_block_rect = pygame.Rect(snake_block.x, snake_block.y, SQUARE_SIZE, SQUARE_SIZE)
            if block_rect.colliderect(snake_block_rect):
                return True
        return False

    def snake_eating_apple(self):
        snake_head=self.snake.get_head()
        apple_rect=pygame.Rect(self.apple.x,self.apple.y,SQUARE_SIZE,SQUARE_SIZE)
        snake_head_rect=pygame.Rect(snake_head.x,snake_head.y,SQUARE_SIZE,SQUARE_SIZE)
        return apple_rect.colliderect(snake_head_rect)

    def outside_board(self,block):
        return block.x < self.offset_x or block.y < self.offset_y or block.x > (BOARD_LENGTH - 1) * SQUARE_SIZE +self.offset_x or block.y > (BOARD_HEIGHT - 1) * SQUARE_SIZE + self.offset_y



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

def distance_between_blocks(block1,block2):
    return abs(block1.x-block2.x)+abs(block1.y-block2.y)








