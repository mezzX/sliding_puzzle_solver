import random
import math
import copy
import numpy as np

def mk_string(board):
    s = ''
    for n in np.nditer(board):
        s += str(int(n))

    return s

class PuzzleSolver():
    def __init__(self):
        self.frontier = {}
        self.explored = {}

    def import_puzzle(self, state):
        self.size = int(math.sqrt(len(state.tiles)))
        self.puzzle = np.zeros((self.size, self.size))
        self.answer = np.zeros((self.size, self.size))
        num = 1
        for r in range(self.size):
            for c in range(self.size):
                self.answer[r][c] = num
                num += 1

        self.answer[-1][-1] = 0

        for tile in state.tiles:
            # current tile position
            c_loc = tile.pos
            # correct tile position
            r_loc = tile.cor_pos
            self.puzzle[c_loc[0]][c_loc[1]] = self.answer[r_loc[0]][r_loc[1]]
        self.frontier[mk_string(self.puzzle)] = [self.score_board(self.puzzle), [], self.puzzle]

    def find_gap(self, board):
        coord = np.argmin(board)
        row = coord // self.size
        col = coord % self.size
        self.gap = (row, col)

    def get_actions(self, board):
        actions = []
        self.find_gap(board)
        if self.gap[1] > 0:
            actions.append('Right')

        if self.gap[0] > 0:
            actions.append('Down')

        if self.gap[1] < self.size - 1:
            actions.append('Left')

        if self.gap[0] < self.size - 1:
            actions.append('Up')

        return actions

    def score_board(self, board):
        scores = []
        for i in range(self.size**2):
           # current tile position
            c_loc = np.where(board == i)
            # correct tile position
            r_loc = np.where(self.answer == i)
            # calculating Manhattan Distance
            y = abs(c_loc[0] - r_loc[0])
            x = abs(c_loc[1] - r_loc[1])
            scores.append(y + x)

        return np.sum(scores)

    def sim_board(self, board, action):
        self.find_gap(board)
        if action == 'Up':
            coords = (self.gap[0]+1, self.gap[1])

        if action == 'Down':
            coords = (self.gap[0]-1, self.gap[1])

        if action == 'Right':
            coords = (self.gap[0], self.gap[1]-1)

        if action == 'Left':
            coords = (self.gap[0], self.gap[1]+1)

        tile = board[coords]
        new_board = copy.copy(board)
        new_board[self.gap] = tile
        new_board[coords] = 0

        return new_board

    def expand(self, key):
        board = self.frontier[key][2]
        actions = self.get_actions(board)
        for action in actions:
            new_board = self.sim_board(board, action)
            new_board_key = mk_string(new_board)
            if new_board_key not in self.frontier.keys() and new_board_key not in self.explored.keys():
                score = self.score_board(new_board)
                move_list = copy.copy(self.frontier[key][1])
                self.frontier[new_board_key] = [score, move_list, new_board]
                self.frontier[new_board_key][1].append(action)
        if key not in self.explored.keys():
            self.explored[key] = copy.deepcopy(self.frontier[key])
        del self.frontier[key]

    def get_total_cost(self, entry):
        # total path cost so far
        g = len(entry[1])
        # estimated remaining path cost
        h = int(entry[0])
        return g + h

    def explore(self):
        boards = {}
        for board in self.frontier.keys():
            cost = self.get_total_cost(self.frontier[board])
            boards[board] = cost
        self.expand(min(boards))
        #self.expand(min(self.frontier, key=lambda x:self.get_total_cost(x)))

    def solve(self, state):
        self.import_puzzle(state)
        while True:
            if mk_string(self.answer) in self.explored.keys():
                print(self.explored[mk_string(self.answer)])
                return self.explored[mk_string(self.answer)][1]
            else:
                self.explore()
                print("{} nodes in the frontier and {} nodes explored".format(len(self.frontier.keys()), len(self.explored.keys())))