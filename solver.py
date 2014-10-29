'''
Handle AI logic for tic-tac-toe game.
'''

from models import Team

# There are only 8 winning cominations for a tic-tac-toe board, so it makes
# more sense to hardcode the values as a constant. This is a list of sets to
# make set operations more convenient.
WINNING_COMBINATIONS = [set(x) for x in [
    [0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 4, 8],
    [0, 3, 6], [1, 4, 7], [2, 5, 8], [2, 4, 6]
]]

def get_winner(board):
    '''
    Determine winner of game.

    Paramaters
        board: Board, board to assess

    Return
        int, Team.FIRST, Team.SECOND, or Team.NEITHER

    '''
    # count spaces beloning to each team
    spaces = {
        Team.FIRST: set([i for i in range(len(board)) if board.get(i) == Team.FIRST]),
        Team.SECOND: set([i for i in range(len(board)) if board.get(i) == Team.SECOND])
    }

    # compare spaces that each team holds to winning combinations
    for combo in WINNING_COMBINATIONS:
        if combo.issubset(spaces[Team.FIRST]):
            return Team.FIRST
        if combo.issubset(spaces[Team.SECOND]):
            return Team.SECOND

    # if loop has finished then no winning combinatinos have been found
    return Team.NEITHER


def get_next_move(board):
    '''
    Make next move according to minimax algorithm.

    Paramaters
        board: Board, board to assess

    Return
        Board, board after move

    '''
    # TODO implement - for now just taking first available space
    return [i for i in range(len(board)) if board.get(i) == Team.NEITHER][0]
