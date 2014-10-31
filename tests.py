'''
Tests for tic tac toe solver.
'''

from models import Board, Team
from solver import get_winner, get_next_move

def test_naive():
    '''
    Test that cpu always defeats a naive player who always takes first
    available space.
    '''
    for cpu in [Team.FIRST, Team.SECOND]:
        board = Board()
        while not get_winner(board):
            if cpu == board.turn():
                board = board.move(get_next_move(board))
            else:
                empty = [i for i in range(len(board)) if not board.get(i)]
                board = board.move(empty[0])

        assert get_winner(board) == cpu

if __name__ == '__main__':
    test_naive()
