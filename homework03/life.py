import pygame
from pygame.locals import *
import random


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
        self.cell_list(True)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_grid()

            # Отрисовка списка клеток
            self.draw_cell_list(self.clist)
            # Выполнение одного шага игры (обновление состояния ячеек)
            self.clist = self.update_cell_list(self.clist)

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def cell_list(self, randomize=True):
        """ Создание списка клеток.

        :param randomize: Если True, то создается список клеток, где
        каждая клетка равновероятно может быть живой (1) или мертвой (0).
        :return: Список клеток, представленный в виде матрицы
        """
        self.clist = []

        self.clist = [[0] * self.cell_width for i in range(self.cell_height)]

        if randomize:
            for i in range(self.cell_height):
                for j in range(self.cell_width):
                    self.clist[i][j] = random.randint(0, 1)

        return self.clist

    def draw_cell_list(self, clist: list) -> None:
        """ Отображение списка клеток

        :param rects: Список клеток для отрисовки,
        представленный в виде матрицы
        """

        for i in range(self.cell_height):
            for j in range(self.cell_width):
                color_cell = pygame.Color('white')

                if clist[i][j] == 1:
                    color_cell = pygame.Color('green')

                rect = Rect(i, j, self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, color_cell, rect)

    def get_neighbours(self, cell: tuple) -> list:
        """ Вернуть список соседей для указанной ячейки

        :param cell: Позиция ячейки в сетке, задается кортежем вида (row, col)
        :return: Одномерный список ячеек, смежных к ячейке cell
        """
        neighbours = []

        dx = [-1, -1, -1, 0, 0, 1, 1, 1]
        dy = [-1, 0, 1, -1, 1, -1, 0, 1]

        x, y = cell
        for i in range(8):
            if x + dx[i] >= 0 and y + dy[i] >= 0:
                tempx = x + dx[i]
                tempy = y + dy[i]
                if tempx < self.cell_height and tempy < self.cell_width:
                    neighbours.append(self.clist[x + dx[i]][y + dy[i]])

        return neighbours

    def update_cell_list(self, cell_list: list) -> list:
        """ Выполнить один шаг игры.

        Обновление всех ячеек происходит одновременно. Функция возвращает
        новое игровое поле.

        :param cell_list: Игровое поле, представленное в виде матрицы
        :return: Обновленное игровое поле
        """

        new_clist = [[0] * self.cell_width for i in range(self.cell_height)]

        for i in range(self.cell_height):
            for j in range(self.cell_width):
                cell = i, j
                neighbours = self.get_neighbours(cell)
                k = 0
                for t in neighbours:
                    if t == 1:
                        k += 1
                if cell_list[i][j] == 0:
                    if k == 3:
                        new_clist[i][j] = 1

                if cell_list[i][j] == 1:
                    if k == 3 or k == 2:
                        new_clist[i][j] = 1
                    if k > 3:
                        new_clist[i][j] = 0

        return new_clist
