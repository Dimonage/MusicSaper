import pygame
import random
import numpy
import sys
import webbrowser
import os

sc = 40
esay_score = 50
medium_score = 160
hard_score = 500
flag_esay = False
flag_medium = False
flag_hard = False

size = width, height = 1000, 700
board_size = [700, 700]
info_size = [width - height, height]
link = 'http://xn--80aafypuh.xn--80aa1agjdchjh2p.xn--p1ai/'
font = 'Times New Roman'
pygame.init()
screen = pygame.display.set_mode(size, pygame.RESIZABLE)
pygame.display.set_caption("Minesweeper")
h1 = pygame.font.SysFont(font, 40)
h2 = pygame.font.SysFont(font, 20)

music = pygame.mixer.music.load('music/One-Love-Emotional-Piano-Strings(chosic.com).mp3')
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1, 0.0)


class Square:
    def __init__(self, state=0):
        self.state = state
        self.number = 1

        self.covered = True
        self.flagged = False

    def show_tiles(self, grid, x):
        if self.flagged:
            return

        self.covered = False
        neighbours = [i for i in
                      [[x[0] - 1, x[1] - 1],
                       [x[0], x[1] - 1],
                       [x[0] + 1, x[1] - 1],
                       [x[0] - 1, x[1]],
                       [x[0] + 1, x[1]],
                       [x[0] - 1, x[1] + 1],
                       [x[0], x[1] + 1],
                       [x[0] + 1, x[1] + 1]]
                      if (0 <= i[0] < len(grid[0]) and 0 <= i[1] < len(grid))]

        for n in neighbours:
            if not grid[n[1]][n[0]].number and grid[n[1]][n[0]].covered:
                grid[n[1]][n[0]].show_tiles(grid, n)
            else:
                grid[n[1]][n[0]].covered = False

class Grid:
    colours = {1: (0, 0, 255),
               2: (50, 205, 50),
               3: (255, 140, 0),
               4: (255, 0, 0),
               5: (148, 0, 211),
               6: (220, 20, 60),
               7: (0, 206, 209),
               8: (255, 105, 180)}

    mine_distribution = 8

 def __init__(self, surf_size, square_size, blit_dest=[0, 0]):
        self.surf = pygame.Surface(surf_size)
        self.resolution = [int(i / square_size) for i in self.surf.get_size()]

        self.size = square_size
        self.blit_dest = blit_dest

        self.generated = False
        self.mines_count = int(numpy.prod(self.resolution) // self.mine_distribution)
        self.flags = self.mines_count

        self.grid = [[Square() for i in range(self.resolution[0])] for i in range(self.resolution[1])]
        self.font = pygame.font.SysFont(font, self.size)