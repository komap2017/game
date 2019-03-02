from game.board import Board
import random


class Explodable:

    def explode(self, board: Board, row: int, column: int):
        raise NotImplementedError('Abstract method!') from None


class Colorable(Explodable):

    def __init__(self, color):
        self.color = color

    def __repr__(self):
        return '{}'.format(self.color)

    def explode(self, board, row, column):
        board[row][column] = None
        return 5

class Lighting(Colorable):

    def explode(self, board, row, column):
        print('got parameters board={}, row={}, column={}'.format(board, row, column))
        board.field[row][column] = None
        for i in range(board.columns):
            cell = board.field[row][i]
            if cell is not None:
                cell.explode(board, row, i)
        for i in range(board.rows):
            cell = board.field[i][column]
            if cell is not None:
                cell.explode(board, i, column)
        return 10

    def __eq__(self, other):
        return self.color == other.color

    def __repr__(self):
        data = super().__repr__()
        template = '|{}|'.format(data)
        return template


class Red(Colorable):

    def __init__(self):
        super().__init__(color='R')


class Green(Colorable):

    def __init__(self):
        super().__init__(color='G')



class Blue(Colorable):

    def __init__(self):
        super().__init__(color='B')


def show_board(board):
    for row in board:
        print(row)
    print()


class Game:


    def __init__(self):
        self.power = 0
        self.activated = False

    @property
    def power(self):
        return self._power

    @power.setter
    def power(self, value):
        if value > 20:
            self._power = 0
            self.activated = True
        else:
            self._power = value

    def process(self, result, board):
        print(result)
        if len(result) < 4:
            summed = sum(result)
        else:
            summed = sum(el * 1.2 for el in result)
        self.power += summed
        if self.activated:
            # print('activated')
            # board[0][0] = Lighting(board[0][0].color)
            self._infect_board(board)
            self.activated = False
    def _infect_board(self, board):
        row = random.randint(0, board.rows - 1)
        column = random.randint(0, board.columns - 1)
        board[row][column] = Lighting(board[row][column].color)


class Processor:

    def __init__(self, board):
        self.board = board
        self._pool = [Red, Green, Blue]
        self.game = Game()

    def process_message(self, message):
        message = message.split(' ')
        command = message[0]
        if command == 'show':
            show_board(self.board)
        elif command == 'rotate':
            numbers = map(int, message[1:])
            numbers = map(lambda x: x - 1, numbers)
            a, b, c, d = numbers
            self.board.rotate((a, b), (c, d))
            res = self.board.check_exploded()
            while len(res) > 0:
                self.board.fall()
                self.board.generate_new(self._pool)
                self.game.process(res, self.board)
                res = self.board.check_exploded()
                # show_board(self.board)
        elif command == 'score':
            print('Score = {}'.format(self.game.power))
        elif command == 'commands' or command == '?':
            self._show_help()
        else:
            raise ValueError('Unknown command {}'.format(message[0]))

    def loop(self):
        while True:
            message = input('command:')
            try:
                self.process_message(message)
            except Exception as e:
                print(e)
            except KeyboardInterrupt:
                print('Exit')
                break

    def _show_help(self):
        for command in ['show', 'rotate', 'commands', 'score']:
            print(command, end=', ')
        print()


def main():
    board = Board(rows=9, columns=9)
    processor = Processor(board)
    processor.board.generate_new(processor._pool)

    p = processor.process_message
    p('show')
    p('rotate 3 2 3 1')
    p('show')
    processor.loop()
    


if __name__ == '__main__':
    main()
