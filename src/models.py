'''
Defines the game board, which is a 3-by-3 square for exactly 2 teams.
'''

class Team:
    '''
    Abstraction that encapsulates the different valid states of a space or
    turn. NEITHER is garunteed to evaluate to False.
    '''
    NEITHER = 0
    FIRST = 1
    SECOND = 2

    @staticmethod
    def other(team):
        '''
        Given a valid team, this method will return the opposite team.

        Parameters
            team: int, either Team.FIRST or Team.SECOND

        Return
            opposite of team

        '''
        return Team.FIRST + Team.SECOND - team


    @staticmethod
    def string(team):
        '''
        Parameters
            team: int, valid Team constant

        Return
            str, representation of team as one-character string

        '''
        if team == Team.FIRST:
            return 'X'
        elif team == Team.SECOND:
            return 'O'
        else:
            return ' '


class Board:
    '''
    Encapsulation of spaces and board state. This class is effectively
    immutable to make recursive operations more intuitive. The Board object
    keeps track of which team will make the next move, but it is unaware of
    conditions for victory. Therefore, a Board object cannot tell if the game
    is over or who has won.
    '''
    SIZE = 3

    def __init__(self, predecessor=None, move=None):
        '''
        Initialize board spaces and current turn state.

        Parameters
            predecessor: Board, board to base copy off

        '''

        if predecessor and move is not None:
            self._spaces = list(predecessor._spaces)  # copy list
            self._spaces[move] = predecessor._turn
            self._turn = Team.other(predecessor._turn)
            self._last = predecessor

        else:
            # board starts with (size * size) empty spaces, belonging to
            # neither team
            self._spaces = [Team.NEITHER for _ in range(Board.SIZE ** 2)]

            # set turn field to team who plays first (always X)
            self._turn = Team.FIRST

            # empty board is its own predecessor, so undo is circular
            self._last = self


    def __iter__(self):
        '''
        Return
            iter, iterator representing values of pieces on board.

        '''
        return iter(self._spaces)


    def __len__(self):
        '''
        Return
            int, number of spaces on board

        '''
        return len(self._spaces)


    def __str__(self):
        '''
        Return
            str, board in printable format.

        '''
        result = tuple(
            [Team.string(space) for space in self._spaces]
        )
        return '\n'.join([
            '     0   1   2',
            '  0  %s | %s | %s ',
            '    -----------',
            '  1  %s | %s | %s ',
            '    -----------',
            '  2  %s | %s | %s ',
            ''
        ]) % result


    def move(self, ind):
        '''
        Take turn as current team in specified position.

        Parameters
            ind: int, index of where to play piece, [0,9)

        Return
            new Board with move

        Raise
            IndexError, ind is out of bounds
            LookupError, space is already occupied

        '''
        # raise exception for invalid move
        if ind < 0 or ind >= Board.SIZE ** 2:
            raise IndexError()
        elif self._spaces[ind]:
            raise LookupError()

        else:
            # proceed with move by making copy for move
            return Board(predecessor=self, move=ind)


    def get(self, team):
        '''
        Get piece in current space

        Parameters
            ind: int, index of space [0,9)

        Return
            int[], indecies of spaces belonging to team

        '''
        return [i for i in range(len(self)) if self._spaces[i] == team]


    def turn(self):
        '''
        Return
            int, Team who will play next

        '''
        return self._turn


    def undo(self):
        '''
        Return
            Board, board with state before last move or itself if board is
                empty

        '''
        return self._last


class Solver:
    '''Define AI logic for cpu player.'''

    # There are only 8 winning cominations for a tic tac toe board, so it
    # makes more sense to hardcode the values as a constant. This is a tuple
    # of sets to make set operations more convenient.
    WINNING_COMBINATIONS = tuple([set(x) for x in [
        [0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 4, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8], [2, 4, 6]
    ]])

    def get_winner(self, board):
        '''
        Determine winner of game.

        Paramaters
            board: Board, board to assess

        Return
            Team constant, Team.FIRST, Team.SECOND, or Team.NEITHER

        '''
        # count spaces beloning to each team
        spaces = {
            Team.FIRST: set(board.get(Team.FIRST)),
            Team.SECOND: set(board.get(Team.SECOND))
        }

        # compare spaces that each team holds to winning combinations
        for combo in Solver.WINNING_COMBINATIONS:
            if combo.issubset(spaces[Team.FIRST]):
                return Team.FIRST
            if combo.issubset(spaces[Team.SECOND]):
                return Team.SECOND

        # if loop has finished then no winning combinatinos have been found
        return Team.NEITHER


    def minimax(self, board, cpu, depth):
        '''
        Scores game state and determines best move for the next play.

        Parameters
            board: Board, board to assess
            cpu: Team constant, cpu team
            depth: number of recurses into future states

        Return
            int, score
            int, best move or -1 if game is over

        '''
        winner = self.get_winner(board)
        if winner == cpu:
            # cpu won game
            return 10 - depth, -1

        elif winner:
            # human won game
            return depth -10, -1

        elif not board.get(Team.NEITHER):
            # tie game
            return 0, -1

        else:
            scores = [(self.minimax(
                board.move(i), cpu, depth + 1)[0], i) for i in board.get(Team.NEITHER)]
            if board.turn() == cpu:
                return max(scores)
            else:
                return min(scores)


    def get_next_move(self, board):
        '''
        Suggest next move according to minimax algorithm. Board must represent an
        ongoing game.

        Paramaters
            board: Board, board to assess

        Return
            int, next move

        '''
        # if board is unplayed, calculations are not worth it
        # just take first slot
        if len(board.get(Team.NEITHER)) == len(board):
            return 0

        else:
            return self.minimax(board, board.turn(), 0)[1]
