import pygame
from pygame.locals import *
import random
from copy import deepcopy


class GameOfLife:

    def __init__(self, width=640, height=480, cell_size=10, speed=10):
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

    def draw_grid(self):
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (0, y), (self.width, y))

    def run(self):
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))

        # Создание списка клеток
        clist = CellList(self.cell_height, self.cell_width, True)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_grid()

            # Отрисовка списка клеток
            self.draw_cell_list(clist)
            # Выполнение одного шага игры (обновление состояния ячеек)
            clist = CellList.update(clist)

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def draw_cell_list(self, clist) -> None:

        for cell in clist:

            color_cell = pygame.Color('white')

            if cell.is_alive():
                color_cell = pygame.Color('green')

            rect = Rect(cell.row * self.cell_size, cell.col * self.cell_size, self.cell_size, self.cell_size)
            pygame.draw.rect(self.screen, color_cell, rect)


class Cell:

    def __init__(self, row=0, col=0, state=False):
        self.row = row
        self.col = col
        self.state = state

    def is_alive(self) -> bool:
        return self.state

    def set_alive(self, state: bool) -> None:
        self.state = state

    def __repr__(self):
        return str(int(self.state))


class CellList:

    def __init__(self, nrows: int, ncols: int, randomize=False,
                 openFile=False, cell_list=[]):
        self.nrows = nrows
        self.ncols = ncols

        if openFile:
            self.clist = cell_list
            return

        self.clist = [[Cell] * ncols for i in range(nrows)]

        for i in range(nrows):
            for j in range(ncols):
                self.clist[i][j] = Cell(i, j, False)

        if randomize:
            for i in range(nrows):
                for j in range(ncols):
                    self.clist[i][j].set_alive(random.randint(0, 1))

    def get_neighbours(self, cell: Cell) -> list:
        neighbours = []
        dx = [-1, -1, -1, 0, 0, 1, 1, 1]
        dy = [-1, 0, 1, -1, 1, -1, 0, 1]

        x = cell.row
        y = cell.col
        for i in range(8):
            if x + dx[i] >= 0 and y + dy[i] >= 0:
                if x + dx[i] < self.nrows and y + dy[i] < self.ncols:
                    neighbours.append(self.clist[x + dx[i]][y + dy[i]])
        return neighbours

    def update(self):
        clist = deepcopy(self)
        new_clist = deepcopy(self)

        for cell in new_clist:
            cell.state = False

        for i in range(self.nrows):
            for j in range(self.ncols):
                neighbours = self.get_neighbours(self.clist[i][j])
                k = 0
                for t in neighbours:
                    if t.is_alive():
                        k += 1

                if not self.clist[i][j].is_alive():
                    if k == 3:
                        new_clist.clist[i][j].set_alive(True)

                if self.clist[i][j].is_alive():
                    if k == 3 or k == 2:
                        new_clist.clist[i][j].set_alive(True)
                    if k > 3:
                        new_clist.clist[i][j].set_alive(False)

        return new_clist

    def __iter__(self):
        self.indexI = 0
        self.indexJ = 0
        return self

    def __next__(self):
        if self.indexI < self.nrows:
            cell = self.clist[self.indexI][self.indexJ]
            self.indexJ += 1
            if (self.indexJ == self.ncols):
                self.indexJ = 0
                self.indexI += 1
            return cell
        else:
            raise StopIteration

    def __str__(self):

        clist = [[0] * self.ncols for i in range(self.nrows)]

        for i in range(self.nrows):
            for j in range(self.ncols):
                clist[i][j] = int(self.clist[i][j].is_alive())

        return str(clist)

    @classmethod
    def from_file(cls, filename: str):

        with open(filename, 'r', encoding='utf-8') as file:
            clist = []
            i = 0
            k = 0
            ncol = 0
            for line in file:
                row = []
                for j in line:
                    if j == "0":
                        row.append(Cell(i, k, False))
                    else:
                        row.append(Cell(i, k, True))
                    ncol = k
                    k += 1

                k = 0
                i += 1
                clist.append(row)

            nrow = i
        return CellList(nrow, ncol, openFile=True, cell_list=clist)


if __name__ == '__main__':
    game = GameOfLife(300, 300, 20)
    game.run()
