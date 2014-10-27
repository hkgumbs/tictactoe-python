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
        int, Team.X, Team.O, or Team.NEITHER

    '''
    # count spaces beloning to each team
    spaces = {
        Team.X: set([space for space in board if space == Team.X]),
        Team.O: set([space for space in board if space == Team.O])
    }

    # DEBUG
    print spaces

    # compare spaces that each team holds to winning combinations
    for combo in WINNING_COMBINATIONS:
        if combo.issubset(spaces[Team.X]): return Team.X
        if combo.issubset(spaces[Team.O]): return Team.O

    # if loop has finished then no winning combinatinos have been found
    return Team.NEITHER
