from constants import *
import copy
import heapq

def convert_block_cords_to_grid_cords(block_x,block_y,snake_direction):
    block_x-=BOARD2_OFFSET_X
    block_y-=BOARD_OFFSET_Y
    match snake_direction:
        case "up":
            return block_y//SQUARE_SIZE,block_x//SQUARE_SIZE
        case "down":
            return (block_y + SQUARE_SIZE - 1) // SQUARE_SIZE, block_x // SQUARE_SIZE
        case "right":
            return block_y // SQUARE_SIZE, (block_x + SQUARE_SIZE - 1) // SQUARE_SIZE
        case "left":
            return block_y  // SQUARE_SIZE, block_x // SQUARE_SIZE
        case "":
            return block_y//SQUARE_SIZE,block_x//SQUARE_SIZE
def get_directions_to_apple(wall,snake,apple):
    snake_head_grid_cords = convert_block_cords_to_grid_cords(snake.get_head_x(), snake.get_head_y() ,snake.get_direction())
    grid=create_grid(wall,snake,apple)
    path=find_shortest_path(grid,(snake_head_grid_cords[0],snake_head_grid_cords[1]),((apple.y-BOARD_OFFSET_Y)//SQUARE_SIZE,(apple.x-BOARD2_OFFSET_X)//SQUARE_SIZE))
    return convert_path_to_directions(path)

def create_grid(wall,snake,apple):
    grid=[]
    for row in range(BOARD_HEIGHT):
        new_row=[]
        for col in range(BOARD_LENGTH):
            new_row.append(0)
        grid.append(new_row)
    return add(grid,wall,snake,apple)

def add(grid,wall,snake,apple):
    grid[(apple.y-BOARD_OFFSET_Y)//SQUARE_SIZE][(apple.x-BOARD2_OFFSET_X)//SQUARE_SIZE]=APPLE
    if wall!=INCONSTRACTABLE:
        for block in wall:
            grid[(block.y-BOARD_OFFSET_Y)//SQUARE_SIZE][(block.x-BOARD2_OFFSET_X)//SQUARE_SIZE]=BARRIER
    snake_head_grid_cords=convert_block_cords_to_grid_cords(snake.get_head_x(),snake.get_head_y(),snake.get_direction())
    grid[snake_head_grid_cords[0]][snake_head_grid_cords[1]]=SNAKE_HEAD
    for block in snake.get_blocks()[1:]:
        block_grid_cords=convert_block_cords_to_grid_cords(block.x,block.y,block.dir)
        grid[block_grid_cords[0]][block_grid_cords[1]]=BARRIER
    for line in grid:
        print(line)
    return grid


def decide_turn_dir(node1,node2):
    row_difference = node1[0] - node2[0]
    col_difference = node1[1]-node2[1]


    if col_difference>0:
        return "left"
    elif col_difference<0:
        return "right"
    elif row_difference>0:
        return "up"
    return "down"


def convert_path_to_directions(path):
    directions=[]
    if path!=None:
        cur_node = path[0]
        for node in path[1:]:
            directions.append(decide_turn_dir(cur_node,node))
            cur_node=copy.copy(node)
    return directions

def find_shortest_path(grid, start, goal):
    open_set = []
    closed_set = set()

    start_node = GridNode(*start)
    goal_node = GridNode(*goal)

    start_node.cost_from_start = 0
    start_node.heuristic_cost_to_goal = get_distance_between_grids(start_node, goal_node)
    start_node.total_cost = start_node.cost_from_start + start_node.heuristic_cost_to_goal

    heapq.heappush(open_set, start_node)

    while open_set:
        current_node = heapq.heappop(open_set)
        if current_node.row == goal_node.row and current_node.col == goal_node.col:
            path = []
            while current_node:
                path.append((current_node.row, current_node.col))
                current_node = current_node.parent

            return path[::-1]
        closed_set.add((current_node.row, current_node.col))

        neighbors = [(current_node.row - 1, current_node.col), (current_node.row + 1, current_node.col), (current_node.row, current_node.col - 1), (current_node.row, current_node.col + 1)]

        for neighbor_row, neighbor_col in neighbors:
            if 0 <= neighbor_row < len(grid) and 0 <= neighbor_col < len(grid[0]) and grid[neighbor_row][neighbor_col] != BARRIER and (neighbor_row, neighbor_col) not in closed_set:

                neighbor_node = GridNode(neighbor_row, neighbor_col)
                neighbor_node.cost_from_start = current_node.cost_from_start + 1
                neighbor_node.heuristic_cost_to_goal = get_distance_between_grids(neighbor_node, goal_node)
                neighbor_node.total_cost = neighbor_node.cost_from_start + neighbor_node.heuristic_cost_to_goal
                neighbor_node.parent = current_node

                if neighbor_node not in open_set:
                    heapq.heappush(open_set, neighbor_node)
    return None


class GridNode:
    def __init__(self,row,col):
        self.row=row
        self.col=col
        self.cost_from_start=0
        self.heuristic_cost_to_goal=0
        self.total_cost=0
        self.parent=None

    def __lt__(self,other):
        return self.total_cost<other.total_cost

def get_distance_between_grids(cur_node, goal_node):
    return abs(cur_node.row-goal_node.row)+abs(cur_node.col-goal_node.col)
