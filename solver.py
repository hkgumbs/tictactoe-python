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
        Team, Team.FIRST, Team.SECOND, or Team.NEITHER

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


def minimax(board, cpu, depth):
    '''
    TODO
    '''
    winner = get_winner(board)
    if winner == cpu:
        # cpu won game
        return 10 - depth, None

    elif winner:
        # human won game
        return depth -10, None

    elif not board.available():
        # tie game
        return 0, None

    else:
        moves = [i for i in range(len(board)) if board.get(i) == Team.NEITHER]
        scores = [
            (minimax(board.move(i), cpu, depth + 1)[0], i) for i in moves
        ]
        if board.turn() == cpu:
            return max(scores)
        else:
            return min(scores)



def get_next_move(board):
    '''
    Make next move according to minimax algorithm.

    Paramaters
        board: Board, board to assess

    Return
        int, next move

    '''
    # if board is unplayed, calculations are not worth it
    # just take first slot
    if board.available() == len(board):
        return 0
    return minimax(board, board.turn(), 0)[1]
