'''
Tests for tic tac toe solver.
'''

from models import Board, Team
from solver import get_winner, get_next_move

def test_naive():
    '''
    Test that cpu always defeats a naive player who always takes first
    available space. Functioned as basic sanity test during production.
    '''
    for cpu in [Team.FIRST, Team.SECOND]:
        # perform test with cpu as both first and second player

        board = Board()
        while not get_winner(board) and board.available():
            # play until winner is determined

            if cpu == board.turn():
                board = board.move(get_next_move(board))

            else:
                # play move on first available space
                board = board.move(board.available()[0])

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


def test_never_lose():
    '''
    Test that cpu player never loses a match.
    '''
    for cpu in [Team.FIRST, Team.SECOND]:
        # perform test with cpu as both first and second player
        never_lose(Board(), cpu)


def never_lose(board, cpu):
    '''
    Descend into every possible game state to determin that cpu player never
    loses.

    Parameters
        board: Board, board to assess
        cpu: Team constant, cpu team
    '''
    winner = get_winner(board)
    if winner == cpu:
        # base case, cpu wins
        return

    elif winner:
        # base case, human wins, should never occur 
        raise AssertionError()

    elif board.available():
        if board.turn() == cpu:
            never_lose(board.move(get_next_move(board)), cpu)
        else:
            for space in board.available():
                # make every possible move
                never_lose(board.move(space), cpu)

    # else tie game

if __name__ == '__main__':
    # test_naive()
    test_two_cpus()
    test_never_lose()
