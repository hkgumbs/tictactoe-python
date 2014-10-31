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
        # perform test with cpu as both first and second player

        board = Board()
        while not get_winner(board):
            # play until winner is determined

            if cpu == board.turn():
                board = board.move(get_next_move(board))

            else:
                # play move on first available space
                empty = [i for i in range(len(board)) if not board.get(i)]
                board = board.move(empty[0])

        # cpu should always win
        assert get_winner(board) == cpu


def test_two_cpus():
    '''
    Test that two cpu players should always end games in a draw.
    '''
    board = Board()
    while board.available():
        # always play the best calculated move
        board = board.move(get_next_move(board))

    # board should end with no winner
    assert not get_winner(board)

if __name__ == '__main__':
    test_naive()
    test_two_cpus()
