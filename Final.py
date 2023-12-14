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

        def generate(self, pos):
            count = 0
            while count < self.mines_count:
                for p, i in enumerate(self.grid):
                    for q, j in enumerate(i):
                        if random.randint(1, self.mine_distribution) == 1 and not \
                                [q, p] in [i for i in [pos,
                                                       [pos[0] - 1, pos[1] - 1],
                                                       [pos[0], pos[1] - 1],
                                                       [pos[0] + 1, pos[1] - 1],
                                                       [pos[0] - 1, pos[1]],
                                                       [pos[0] + 1, pos[1]],
                                                       [pos[0] - 1, pos[1] + 1],
                                                       [pos[0], pos[1] + 1],
                                                       [pos[0] + 1, pos[1] + 1]]
                                           if (0 <= i[0] < len(self.grid[0]) and
                                               0 <= i[1] < len(self.grid))] and not \
                                j.number == -1 and count < self.mines_count:
                            j.number = -1
                            count += 1

            for y, row in enumerate(self.grid):
                for x, col in enumerate(row):
                    surrounding_mines = 0

                    if col.number == -1:
                        continue

                    combinations = [[x - 1, y - 1], [x, y - 1], [x + 1, y - 1], [x - 1, y], [x + 1, y], [x - 1, y + 1],
                                    [x, y + 1], [x + 1, y + 1]]
                    for combination in combinations:
                        if 0 <= combination[0] < len(self.grid[0]) and 0 <= combination[1] < len(self.grid):
                            if self.grid[combination[1]][combination[0]].number == -1:
                                surrounding_mines += 1

                    col.number = surrounding_mines

            self.generated = True

        def tile_click(self, pos, button):
            grid_x = self.coords_to_grid_x(pos)

            if grid_x is None:
                return
            if not self.generated:
                self.generate(grid_x)

            if button == 1 and not self.grid[grid_x[1]][grid_x[0]].flagged:
                if self.grid[grid_x[1]][grid_x[0]].number:
                    self.grid[grid_x[1]][grid_x[0]].covered = False
                else:
                    self.grid[grid_x[1]][grid_x[0]].show_tiles(self.grid, grid_x)
            elif button == 3:
                if self.flags > 0 and not self.grid[grid_x[1]][grid_x[0]].flagged:
                    self.grid[grid_x[1]][grid_x[0]].flagged = True
                elif self.grid[grid_x[1]][grid_x[0]].flagged:
                    self.grid[grid_x[1]][grid_x[0]].flagged = False

                self.flags = self.mines_count - sum(sum(i.flagged for i in row) for row in self.grid)

    def coords_to_grid_x(self, pos):
        if all(x < self.resolution[p] for p, x in
               enumerate([int((pos[i] - self.blit_dest[i]) // self.size) for i in range(2)])):
            return [int((pos[i] - self.blit_dest[i]) // self.size) for i in range(2)]
        else:
            return None

    def draw(self, surf):
        for y, row in enumerate(self.grid):
            for x, square in enumerate(row):
                if not square.covered:
                    pygame.draw.rect(self.surf, (255, 255, 255), (x * self.size, y * self.size, self.size, self.size),
                                     0)

                    if square.number == -1:
                        pygame.draw.circle(self.surf, (255, 0, 0),
                                           [int(x * self.size + (self.size / 2)), int(y * self.size + (self.size / 2))],
                                           int(self.size / 4), 0)
                    elif square.number:
                        message = self.font.render(str(square.number), True, self.colours[square.number])
                        self.surf.blit(message, message.get_rect(
                            center=[x * self.size + (self.size / 2), y * self.size + (self.size / 2)]))
                else:
                    pygame.draw.rect(self.surf, (150, 150, 150), (x * self.size, y * self.size, self.size, self.size),
                                     0)

                    if square.flagged:
                        pygame.draw.polygon(self.surf, (255, 0, 0),
                                            [[x * self.size + (0.3 * self.size), y * self.size + (0.2 * self.size)],
                                             [x * self.size + (0.4 * self.size), y * self.size + (0.2 * self.size)],
                                             [x * self.size + (0.4 * self.size), y * self.size + (0.22 * self.size)],
                                             [x * self.size + (0.8 * self.size), y * self.size + (0.4 * self.size)],
                                             [x * self.size + (0.4 * self.size), y * self.size + (0.6 * self.size)],
                                             [x * self.size + (0.4 * self.size), y * self.size + (0.8 * self.size)],
                                             [x * self.size + (0.3 * self.size), y * self.size + (0.8 * self.size)]], 0)

        for x in range(1, len(self.grid[0])):
            pygame.draw.line(self.surf, (0, 0, 0), [x * self.size, 0], [x * self.size, surf.get_height()], 1)
        for y in range(1, len(self.grid)):
            pygame.draw.line(self.surf, (0, 0, 0), [0, y * self.size], [surf.get_width(), y * self.size], 1)

        surf.blit(self.surf, self.blit_dest)

    def game_status(self):
            if not any(
                    any(
                        (s.flagged and not s.number == -1) or (not s.flagged and s.number == -1) for s in row_) for row_
                    in
                    self.grid) and all(
                all(not t.covered or (t.covered and t.flagged) for t in _row) for _row in self.grid):
                return True
            elif any(
                    any(g.number == -1 and not g.covered for g in row) for row in self.grid):
                return False
            else:
                return None

    def reset(self, square_size=None):
            if square_size is not None:
                self.resolution = [int(i / square_size) for i in self.surf.get_size()]
                self.size = square_size
                self.mines_count = int(numpy.prod(self.resolution) // self.mine_distribution)
                self.font = pygame.font.SysFont(font, self.size)

            self.grid = [[Square() for _ in range(self.resolution[0])] for _ in range(self.resolution[1])]
            self.generated = False
            self.flags = self.mines_count


class Info:

    def __init__(self, surf_size, grid, blit_dest):
        self.grid = grid
        self.surf = pygame.Surface(surf_size)

        self.t = pygame.time.get_ticks()
        self.blit_dest = blit_dest
        self.h1 = pygame.font.SysFont(font, 50)
        self.h2 = pygame.font.SysFont(font, 30)

    def update(self):
        self.surf.fill((250, 250, 255))
        pygame.draw.line(self.surf, (0, 0, 0), [0, 0], [0, self.surf.get_height()], 1)

        image1 = pygame.image.load(os.path.join('foto/photo.jpg'))
        image11 = pygame.transform.scale(image1, (200, 200))
        self.surf.blit(image11, (50, 450))

        score = self.h2.render("best score: {}".format(sc), False, (0, 0, 0))
        self.surf.blit(score, score.get_rect(center=[self.surf.get_width() / 2, self.surf.get_height() / 5]))

        flag = self.h2.render("Flags: {}/{}".format(self.grid.flags, self.grid.mines_count), True, (0, 0, 0))
        self.surf.blit(flag, flag.get_rect(center=[self.surf.get_width() / 2, self.surf.get_height() / 2 - 50]))

        time_ = self.h2.render("Time: {}".format(int(pygame.time.get_ticks() - self.t) // 1000), True, (0, 0, 0))
        self.surf.blit(time_, time_.get_rect(center=[self.surf.get_width() / 2, self.surf.get_height() / 2]))

        levels = {100: "Easy",
                  50: "Medium",
                  25: "Hard"}
        difficulty = self.h2.render("Difficulty: {}".format(levels[self.grid.size]), True, (0, 0, 0))
        self.surf.blit(difficulty, difficulty.get_rect(center=[self.surf.get_width() / 2,
                                                               self.surf.get_height() / 2 + 50]))

    def draw(self, surf):
        surf.blit(self.surf, self.blit_dest)

    def reset(self):
        self.t = pygame.time.get_ticks()

