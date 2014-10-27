'''
Handle IO for tic-tac-toe game.
'''

from models import Board


def print_board(board):
    board_flattened = tuple([
        board.get(i, j) for i in range(BOARD_SIZE) for j in range(BOARD_SIZE)
    ])
    print '\n'.join([
        ' %s | %s | %s ',
        '-----------',
        ' %s | %s | %s ',
        '-----------',
        ' %s | %s | %s ',
    ]) % board_flattened


def main():
    '''
    Control and loop game indefeinitely until user quits.
    '''
    print 'Welcome to un anbeatable tic-tac-toe game!'
    print '\n'

    board = Board()
    next_move = None
    while not next_move:


if __name__ == '__main':
    main()
