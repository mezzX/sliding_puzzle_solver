from tkinter import filedialog
from tkinter import *
from tkinter.ttk import Entry, Button, OptionMenu
from PIL import Image, ImageTk
import random
import os
import solver

class Tiles():
    def __init__(self, grid):
        self.tiles = []
        self.grid = grid
        self.gap = None
        self.moves = 0

    def add(self, tile):
        self.tiles.append(tile)

    def shuffle(self):
        random.shuffle(self.tiles)
        i = 0
        for row in range(self.grid):
            for col in range(self.grid):
                self.tiles[i].pos = (row, col)
                i += 1

    def show(self):
        for tile in self.tiles:
            if tile != self.gap:
                tile.show()

    def set_gap(self, index):
        self.gap = self.tiles[index]

    def is_correct(self):
        for tile in self.tiles:
            if not tile.is_correct_pos():
                return False

        return True

    def get_tile(self, *pos):
        for tile in self.tiles:
            if tile.pos == pos:
                return tile

    def get_tiles_by_gap(self):
        gap_r, gap_c = self.gap.pos

        return self.get_tile(gap_r, gap_c-1), self.get_tile(gap_r-1, gap_c), self.get_tile(gap_r, gap_c+1), self.get_tile(gap_r+1, gap_c)

    def move_gap(self, tile):
        try:
            gap_p = self.gap.pos
            self.gap.pos = tile.pos
            tile.pos = gap_p
            self.moves += 1
        except AttributeError:
            pass

    def slide(self, key):
        left, up, right, down = self.get_tiles_by_gap()
        if key == 'Up':
            self.move_gap(down)
        elif key == 'Down':
            self.move_gap(up)
        elif key == 'Right':
            self.move_gap(left)
        elif key == 'Left':
            self.move_gap(right)
        self.show()


class Tile(Label):
    def __init__(self, parent, image, pos):
        Label.__init__(self, parent, image=image)

        self.image = image
        self.pos = pos
        self.cor_pos = pos

    def show(self):
        self.grid(row=self.pos[0], column=self.pos[1])

    def is_correct_pos(self):
        return self.pos == self.cor_pos


class Board(Frame):   
    MAX_BOARD_SIZE = 500

    def __init__(self, parent, image, grid, win, restart, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)

        self.parent = parent
        self.grid = grid
        self.win = win
        self.restart = restart
        self.solver = solver.PuzzleSolver()
        self.image = self.open_image(image)
        self.tile_size = self.image.size[0] / self.grid
        self.tiles = self.create_tiles()
        self.tiles.shuffle()
        self.tiles.show()
        self.bind_keys()

    def open_image(self, image):
        image = Image.open(image)
        if min(image.size) > self.MAX_BOARD_SIZE:
            image = image.resize((self.MAX_BOARD_SIZE, self.MAX_BOARD_SIZE), Image.ANTIALIAS)
        if image.size[0] != image.size[1]:
            image = image.crop((0, 0, image.size[0], image.size[0]))

        return image

    def create_tiles(self):
        tiles = Tiles(self.grid)
        for row in range(self.grid):
            for col in range(self.grid):
                x0 = col * self.tile_size
                y0 = row * self.tile_size
                x1 = x0 + self.tile_size
                y1 = y0 + self.tile_size
                tile_image = ImageTk.PhotoImage(self.image.crop((x0, y0, x1, y1)))
                tile = Tile(self, tile_image, (row, col))
                tiles.add(tile)
        tiles.set_gap(-1)

        return tiles

    def bind_keys(self):
        self.bind_all('<Key-Up>', self.slide)
        self.bind_all('<Key-Down>', self.slide)
        self.bind_all('<Key-Right>', self.slide)
        self.bind_all('<Key-Left>', self.slide)
        self.bind_all('<Key-r>', self.restart)
        self.bind_all('<Key-s>', self.solve)

    def solve(self, event):
        actions = self.solver.solve(self.tiles)
        for action in actions:
            #root.after(500, self.tiles.slide(action))
            self.tiles.slide(action)
        if self.tiles.is_correct():
            self.win(self.tiles.moves)

    def slide(self, event):
        self.tiles.slide(event.keysym)
        if self.tiles.is_correct():
            self.win(self.tiles.moves)


class Puzzle():
    def __init__(self, parent):
        self.parent = parent

        self.image = StringVar()
        self.win_text = StringVar()
        self.grid = IntVar()

        self.create_widgets()

    def create_widgets(self):
        self.mainFrame = Frame(self.parent)
        Label(self.mainFrame, text='Sliding Puzzle', font=('',50)).pack(padx=10, pady=10)
        frame = Frame(self.mainFrame)
        Label(frame, text='Image').grid(sticky=W)
        Entry(frame, textvariable=self.image, width=50).grid(row=0, column=1, padx=10, pady=10)
        Button(frame, text='Browse', command=self.browse).grid(row=0, column=2, pady=10)
        Label(frame, text='Grid').grid(sticky=W)
        OptionMenu(frame, self.grid, *[3,3,4,5,6,7,8,9,10]).grid(row=1, column=1, padx=10, pady=10, sticky=W)
        frame.pack()
        Button(self.mainFrame, text='Start', command=self.start).pack(padx=10, pady=10)
        self.mainFrame.pack()
        self.board = Frame(self.parent)
        self.winFrame = Frame(self.parent)
        Label(self.winFrame, textvariable=self.win_text, font=('', 50)).pack(padx=10, pady=10)
        Button(self.winFrame, text='Play Again', command=self.play_again).pack(padx=10, pady=10)

    def start(self):
        image = self.image.get()
        grid = self.grid.get()
        if os.path.exists(image):
            self.board = Board(self.parent, image, grid, self.win, self.restart)
            self.mainFrame.pack_forget()
            self.board.pack()

    def restart(self, event):
        self.board.pack_forget()
        self.mainFrame.pack()

    def browse(self):
        self.image.set(filedialog.askopenfilename(title='Select Image', filetype=(('png File','*.png'),('jpg File','*.jpg'))))

    def win(self, moves):
        self.board.pack_forget()
        self.win_text.set('Puzzle Solved in {} moves'.format(moves))
        self.winFrame.pack()

    def play_again(self):
        self.winFrame.pack_forget()
        self.mainFrame.pack()


if __name__ =='__main__':
    root = Tk()
    Puzzle(root)
    root.mainloop()