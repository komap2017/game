from ..board import Board
import pytest


class Number:

    def __init__(self, data):
        self.data = data
        self.exploded = 0
        self.color = data

    def explode(self, board, row, column):
        self.exploded += 1
        self.row = row
        self.column = column

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value

    def __eq__(self, other):
        return self.data == other.data

    def __repr__(self):
        return str(self.data)


class Lighting:

    def __init__(self, color):
        self.color = color
        self.called = False
    def explode(self, board, row, column):
        self.called = True
        print('got parameters board={}, row={}, column={}'.format(board, row, column))
        for i in range(board.columns):
            board.field[row][i] = None
        for i in range(board.rows):
            board.field[i][column] = None
    def __eq__(self, other):
        return self.color == other.color


def test_rotate():
    template = '''1 4 3 6
                  4 2 4 7
                  5 5 1 8
                  9 10 11 12
                '''
    numbers = [Number(int(el)) for el in template.split(' ') if len(el) > 0]
    print(numbers)
    board = Board(rows=4, columns=4)
    for cell in numbers:
        board.fill_empty(cell)

    board.rotate((0, 1), (1, 1))
    num = Number(4)
    assert board[1][0] == num
    assert board[1][1] == num
    assert board[1][2] == num


def test_check_exploded():
    template = '''4 4 3 4
                  4 4 4 4
                  4 4 1 4
                  4 4 11 4
                '''
    numbers = [Number(int(el)) for el in template.split(' ') if len(el) > 0]
    board = Board(rows=4, columns=4)
    for cell in numbers:
        board.fill_empty(cell)
    board.check_exploded()
    num = Number(4)
    for number in numbers:
        if number == num:
            assert number.exploded == 1
        else:
            assert number.exploded == 0


def test_lighting():
    template = '''l 5 2
                  4 2 4
                  2 1 2
                '''
    numbers = [Number(el.strip()) for el in template.split(' ') if len(el) > 0]
    numbers[0] = Lighting('2')
    assert numbers[0].color == numbers[2].color
    board = Board(rows=3, columns=3)
    for cell in numbers:
        board.fill_empty(cell)
    board.rotate((1, 1), (0, 1))
    board.check_exploded()
    assert numbers[0].called
    assert board[0][0] is None
    assert board[0][1] is None
    assert board[0][2] is None
    assert board[1][0] is None
    assert board[2][0] is None


def test_fall():
    template = '''1 2 3
                5 6 4
                8 7 5
                '''
    numbers = [Number(el.strip()) for el in template.split(' ') if len(el) > 0]
    board = Board(rows=3, columns=3)
    for cell in numbers:
        board.fill_empty(cell)
    board[2][0] = None
    board[2][1] = None
    board.fall()
    assert board[1][0] == numbers[0]
    assert board[1][1] == numbers[1]
    assert board[2][0] == numbers[3]
    assert board[2][1] == numbers[4]
    assert board[0][0] is None
    assert board[0][1] is None

    
def test_generate_new():
    board = Board(rows=2, columns=2)
    first = Number(1)
    second = Number(2)
    third = Number(3)
    for cell in [first, second, third]:
        board.fill_empty(cell)
    assert board[1][1] is None
    pool =  [lambda : Number(4), lambda : Number(5)]
    board.generate_new(pool)
    element = board[1][1]
    assert element == Number(4) or element == Number(5)
