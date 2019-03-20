import random
import math
import copy
import numpy as np

class PuzzleSolver():
    def __init(self, size):
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
        self.frontier[self.puzzle] = [self.score_board(self.puzzle), []]

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
        for i in range(9):
           # current tile position
            c_loc = np.where(board == i)
            # correct tile position
            r_loc = np.where(self.answer == i)
            #calculating Manhattan Distance
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

    def expand(self, board):
        actions = self.get_actions(board)
        for action in actions:
            new_board = self.sim_board(board, action)
            score = self.score_board(new_board)
            self.frontier[new_board] = [score, self.frontier[board][1]]
            self.frontier[new_board][1].append(action)
        self.explored[board] = self.frontier[board]
        del self.frontier[board]

    def eval_actions(self, state):
        scores = {}
        actions = self.get_actions(state)
        for action in actions:
            print(action)
            board = self.sim_board(state, action)
            score = self.score_board(board)
            scores[action] = score

        return scores

    def choose_action(self, state):
        self.import_puzzle(state)
        actions = self.eval_actions(self.puzzle)
        best_val = float('inf')
        action = ''
        for direction in actions.keys():
            if actions[direction] < best_val:
                action = direction
                best_val = actions[direction]

        print(actions)
        print(action)

        return action

    def get_total_cost(self, entry):
        #total path cost so far
        g = len(entry[1])
        #estimated remaining path cost
        h = entry[0]
        return g + h

    def explore(self):
        self.expand(min(self.frontier, key=lambda x:self.get_total_cost(x)))

    def solve(self, state):
        self.import_puzzle(state)
        while True:
            if self.answer in self.explored.key():
                return self.explored[self.answer][1]
            else:
                self.explore()