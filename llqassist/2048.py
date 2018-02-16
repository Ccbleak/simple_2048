import os

import readchar
import numpy as np

import statemachine


def start_game(game_grid):
    """action with start game"""

    game_grid = generate_next_num(game_grid)
    game_grid = generate_next_num(game_grid)
    os.system('clear')
    show_grid(game_grid)
    newState = "Continue"
    return newState, game_grid


def continue_game(game_grid):
    """action with continue game"""

    print("输入wasd控制移动方向，q退出游戏：")
    command = readchar.readchar()
    old_grid = game_grid.copy()
    list1 = ["W", "A", "S", "D", "Q"]
    if command.upper() in list1:
        game_grid = move_action(game_grid, command.upper())  # grid move
    if np.all(game_grid == 0):
        newState = "End"
    elif np.all(old_grid == game_grid):
        newState = "Continue"
    else:
        # generate new num in grid
        game_grid = generate_next_num(game_grid)
        if can_be_continue(game_grid):  # judge continue state
            newState = "Continue"
        else:
            newState = "End"
        os.system('clear')
        show_grid(game_grid)
    return newState, game_grid
      

def generate_next_num(grid):
    """choose the next position and generate 2 or 4"""

    zero_position = np.argwhere(grid == 0)
    next_index = np.random.randint(zero_position.shape[0])
    grid[zero_position[next_index][0]][zero_position[next_index][1]] = np.random.randint(1, 3) * 2
    return grid


def can_be_continue(grid):
    """judge if game can continue"""

    grid_size = grid.shape[0]
    State = False
    if 0 in grid:
        State = True
    else:
        for i in range(grid_size):
            line = grid[i]
            for prev, nex in zip(line[0:-1], line[1:]):
                if prev == nex:
                    State = True
                    break
            column = grid[:, i]
            for prev, nex in zip(column[0:-1], column[1:]):
                if prev == nex:
                    State = True
                    break
            if State == True:
                break
    return State


def move_action(grid, command='W'):
    """shift action with 'WASDQ' """

    grid_size = grid.shape[0]
    if command in 'Q':
        grid = np.zeros((grid_size, grid_size), dtype=int)
    if command in 'WS':
        grid = grid.T
    for i in range(grid_size):
        line = grid[i]
        linenew = []
        if command in 'SD':
            line = line[::-1]
        line = np.delete(line, np.where(line == 0))
        j = 0
        while j < line.shape[0]-1:
            if line[j] == line[j+1]:
                linenew.append(line[j]*2)
                j += 2
            else:
                linenew.append(line[j])
                j += 1
        if j == line.shape[0]-1:
            linenew.append(line[j])
        while len(linenew) < grid_size:
            linenew.append(0)
        if command in 'SD':
            linenew = linenew[::-1]
        grid[i] = linenew
    if command in 'WS':
        grid = grid.T
    return grid


def show_grid(grid):
    """draw the grid"""

    grid_size = grid.shape[0]
    output = ''

    # draw the emepty grid
    for i in range(grid_size):
        output += ('+' + '-' * 6) * grid_size
        output += '+\n'
        output += ('|' + ' ' * 6) * grid_size
        output += '|\n'

    output += ('+' + '-' * 6) * grid_size
    output += '+'

    output = list(output)
    x_list, y_list = np.where(grid != 0)

    for x, y in zip(x_list, y_list):
        # find the position to fill the non-zero number
        rect_position = (7 * grid_size + 2) * (2 * x + 1) + 7 * y + 5
        num = grid[x, y]
        while True:
            last_ch = str(num % 10)
            num //= 10
            output[rect_position] = last_ch
            rect_position -= 1

            if num == 0:
                break

    output = ''.join(output)
    print(output)


if __name__== "__main__":
    m = statemachine.StateMachine()
    m.add_state("Start", start_game)  # add start action
    m.add_state("Continue", continue_game)  # add continue action
    m.add_state("End",None, end_state=1)  # add end action
    m.set_start("Start")

    grid_size = 4
    start_grid = np.zeros((grid_size, grid_size), dtype=int)
    m.run(start_grid)