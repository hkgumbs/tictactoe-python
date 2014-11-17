'''
Tests for tic tac toe solver.
'''

from models import Board, Team, Solver

def test_naive():
    '''
    Test that cpu always defeats a naive player who always takes first
    available space. Functioned as basic sanity test during production.
    '''
    for cpu in [Team.FIRST, Team.SECOND]:
        # perform test with cpu as both first and second player

        board = Board()
        solver = Solver()
        while not solver.get_winner(board) and board.get(Team.NEITHER):
            # play until winner is determined

            if cpu == board.turn():
                board = board.move(solver.get_next_move(board))

            else:
                # play move on first available space
                board = board.move(board.get(Team.NEITHER)[0])

        # cpu should always win
        assert solver.get_winner(board) == cpu


def test_two_cpus():
    '''
    Test that two cpu players should always end games in a draw.
    '''
    board = Board()
    solver = Solver()
    while board.get(Team.NEITHER):
        # always play the best calculated move
        board = board.move(solver.get_next_move(board))

    # board should end with no winner
    assert not solver.get_winner(board)


def test_never_lose():
    '''
    Test that cpu player never loses a match.
    '''
    for cpu in [Team.FIRST, Team.SECOND]:
        # perform test with cpu as both first and second player
        never_lose(Board(), Solver(), cpu)


def never_lose(board, solver, cpu):
    '''
    Descend into every possible game state to determin that cpu player never
    loses.

    Parameters
        board: Board, board to assess
        cpu: Team constant, cpu team
    '''
    winner = solver.get_winner(board)
    if winner == cpu:
        # base case, cpu wins
        return

    elif winner:
        # base case, human wins, should never occur 
        raise AssertionError()

    elif board.get(Team.NEITHER):
        if board.turn() == cpu:
            never_lose(board.move(solver.get_next_move(board)), solver, cpu)
        else:
            for space in board.get(Team.NEITHER):
                # make every possible move
                never_lose(board.move(space), solver, cpu)

    # else tie game

if __name__ == '__main__':
    # test_naive()
    test_two_cpus()
    test_never_lose()
