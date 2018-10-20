import math


def read_sudoku(filename):
    """ Прочитать Судоку из указанного файла """
    digits = [c for c in open(filename).read() if c in '123456789.']
    grid = group(digits, 9)
    return grid


def display(values):
    """Вывод Судоку """
    width = 2
    line = '+'.join(['-' * (width * 3)] * 3)
    for row in range(9):
        print(''.join(values[row][col].center(width) + ('|' if str(col) in '25' else '') for col in range(9)))
        if str(row) in '25':
            print(line)
    print()


def group(values: list, n: int) -> list:
    """
    Сгруппировать значения values в список, состоящий из списков по n элементов
    >>> group([1,2,3,4], 2)
    [[1, 2], [3, 4]]
    >>> group([1,2,3,4,5,6,7,8,9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """

    mat = [[0] * n for i in range(n)]
    j = -1
    for i in range(len(values)):

        if i % n == 0:
            j += 1

        mat[j][i % n] = values[i]
    return mat


def get_row(values, pos):
    """ Возвращает все значения для номера строки, указанной в pos
    >>> get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '2', '.']
    >>> get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0))
    ['4', '.', '6']
    >>> get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0))
    ['.', '8', '9']
    """
    return values[pos[0]]


def get_col(values, pos):
    """ Возвращает все значения для номера столбца, указанного в pos
    >>> get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1))
    ['2', '.', '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2))
    ['3', '6', '9']
    """

    col = []
    for i in values:
        col.append(i[pos[1]])
    return col


def get_block(values, pos):
    """ Возвращает все значения из квадрата, в который попадает позиция pos
    >>> grid = read_sudoku('puzzle1.txt')
    >>> get_block(grid, (0, 1))
    ['5', '3', '.', '6', '.', '.', '.', '9', '8']
    >>> get_block(grid, (4, 7))
    ['.', '.', '3', '.', '.', '1', '.', '.', '6']
    >>> get_block(grid, (8, 8))
    ['2', '8', '.', '.', '.', '5', '.', '7', '9']
    """

    matrix = []
    big_m = []
    for k in range(len(values)):

        n = int(math.sqrt(len(values[k])))

        val = values[k]

        mat = [[0] * n for i in range(n)]
        j = -1

        for i in range(len(val)):

            if i % n == 0:
                j += 1

            mat[j][i % n] = val[i]
        big_m.append(mat)

    j = pos[1] // n

    t = (pos[0] // n + 1) * n - 1
    t1 = (pos[0] // n) * n - 1
    for i in range(t1 + 1, t + 1):
        matrix.append(big_m[i][j])

    res = []
    for i in range(n):
        for j in range(n):
            res.append(matrix[i][j])

    return res


def find_empty_positions(grid):
    """ Найти первую свободную позицию в пазле
    >>> find_empty_positions([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']])
    (0, 2)
    >>> find_empty_positions([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']])
    (1, 1)
    >>> find_empty_positions([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']])
    (2, 0)
    """

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == ".":
                return i, j


def find_possible_values(grid, pos):
    """ Вернуть множество возможных значения для указанной позиции
    >>> grid = read_sudoku('puzzle1.txt')
    >>> values = find_possible_values(grid, (0,2))
    >>> values == {'1', '2', '4'}
    True
    >>> values = find_possible_values(grid, (4,7))
    >>> values == {'2', '5', '9'}
    True
    """

    big_m = []
    for k in range(len(grid)):

        n = int(math.sqrt(len(grid[k])))

        val = grid[k]

        mat = [[0] * n for i in range(n)]
        j = -1

        for i in range(len(val)):

            if i % n == 0:
                j += 1

            mat[j][i % n] = val[i]
        big_m.append(mat)

    all_num = set("123456789")
    r = set(get_row(grid, pos))
    b = set(get_block(grid, pos))
    c = set(get_col(grid, pos))
    res = all_num - r - b - c

    return res


def solve(grid):

    pass


def check_solution(solution):
    """ Если решение solution верно, то вернуть True, в противном случае False """
    # TODO: Add doctests with bad puzzles
    pass


def generate_sudoku(N):
    pass


if __name__ == '__main__':
    for fname in ['puzzle1.txt']:
        grid = read_sudoku(fname)
        display(grid)
