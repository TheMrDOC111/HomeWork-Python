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
    mat = [[0] * n for i in range(n)]
    j = -1
    for i in range(len(values)):

        if i % n == 0:
            j += 1

        mat[j][i % n] = values[i]
    return mat


def get_row(values, pos):
    return values[pos[0]]


def get_col(values, pos):
    l = []
    for i in range(int(math.sqrt(len(values)))):
        l.append(values[i][pos[1]])
    return l


def get_block(values, pos):
    # print(values)
    l = []
    bigM = []
    for k in range(len(values)):

        n = int(math.sqrt(len(values[k])))

        val = values[k]

        mat = [[0] * n for i in range(n)]
        j = -1

        for i in range(len(val)):

            if i % n == 0:
                j += 1

            mat[j][i % n] = val[i]
        # print(k, " ", mat)
        bigM.append(mat)

    # print(bigM)
    # print(bigM[pos[0]][pos[1]//n])
    # print(bigM[1][1])

    j = pos[1] // n

    t = (pos[0] // n + 1) * n - 1
    t1 = (pos[0] // n) * n - 1
    for i in range(t1 + 1, t + 1):
        l.append(bigM[i][j])

    res = []
    for i in range(n):
        for j in range(n):
            res.append(l[i][j])

    return res


def find_empty_positions(grid):
    """ Найти первую свободную позицию в пазле

     find_empty_positions([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']])
    (0, 2)
     find_empty_positions([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']])
    (1, 1)
     find_empty_positions([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']])
    (2, 0)
    """
    pass


def find_possible_values(grid, pos):
    """ Вернуть множество возможных значения для указанной позиции

     grid = read_sudoku('puzzle1.txt')
     values = find_possible_values(grid, (0,2))
     values == {'1', '2', '4'}
    True
     values = find_possible_values(grid, (4,7))
     values == {'2', '5', '9'}
    True
    """
    pass


def solve(grid):
    """ Решение пазла, заданного в grid """
    """ Как решать Судоку?
        1. Найти свободную позицию
        2. Найти все возможные значения, которые могут находиться на этой позиции
        3. Для каждого возможного значения:
            3.1. Поместить это значение на эту позицию
            3.2. Продолжить решать оставшуюся часть пазла

     grid = read_sudoku('puzzle1.txt')
     solve(grid)
    [['5', '3', '4', '6', '7', '8', '9', '1', '2'], ['6', '7', '2', '1', '9', '5', '3', '4', '8'], ['1', '9', '8', '3', '4', '2', '5', '6', '7'], ['8', '5', '9', '7', '6', '1', '4', '2', '3'], ['4', '2', '6', '8', '5', '3', '7', '9', '1'], ['7', '1', '3', '9', '2', '4', '8', '5', '6'], ['9', '6', '1', '5', '3', '7', '2', '8', '4'], ['2', '8', '7', '4', '1', '9', '6', '3', '5'], ['3', '4', '5', '2', '8', '6', '1', '7', '9']]
    """
    pass


def check_solution(solution):
    """ Если решение solution верно, то вернуть True, в противном случае False """
    # TODO: Add doctests with bad puzzles
    pass


def generate_sudoku(N):
    """ Генерация судоку заполненного на N элементов

     grid = generate_sudoku(40)
     sum(1 for row in grid for e in row if e == '.')
    41
     solution = solve(grid)
     check_solution(solution)
    True
     grid = generate_sudoku(1000)
     sum(1 for row in grid for e in row if e == '.')
    0
     solution = solve(grid)
     check_solution(solution)
    True
     grid = generate_sudoku(0)
     sum(1 for row in grid for e in row if e == '.')
    81
     solution = solve(grid)
     check_solution(solution)
    True
    """
    pass


if __name__ == '__main__':
    for fname in ['puzzle1.txt', 'puzzle2.txt', 'puzzle3.txt']:
        grid = read_sudoku(fname)
        display(grid)
        print(get_block(grid, (8, 8)))
        # solution = solve(grid)
        #  display(solution)
