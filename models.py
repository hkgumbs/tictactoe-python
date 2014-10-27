'''
Defines the unbeatable tic-tac-toe game with exactly 2 teams and a square
board of variable width.
'''

class Team:
    '''
    Constants that represent the different valid states of a space or turn.
    '''
    NEITHER = None
    X = 1
    O = 2


    def next(team):
        '''
        Given a valid team, this method will return the opposite team.

        Parameters
            team: int, either Team.X or Team.O

        Return
            opposite of team

        '''
        return Team.X + Team.O - team


class Board:
    '''
    Encapsulation of spaces and board state. This class is immutable to make
    recursive operations more intuitive. The Board object keeps track of which
    team will make the next move, but it is unaware of conditions for victory.
    Therefore, a Board object cannot tell if the game is over or who has won.
    '''


    def __init__(self, size=3, copy=None):
        '''
        Initialize board spaces and current turn state.

        Parameters
            size: int, dimmensions for new (size * size) board
            copy: Board, board to copy
        '''

        if copy:
            self.__spaces__ = [list(row) for row in copy.__spaces__]
            self.__turn__ = copy.__turn__

        else:
            # board starts with (size * size) empty spaces, belonging to
            # neither team
            self.__spaces__ = [
                [Team.NEITHER for _ in range(size)] for _ in range(size)
            ]

            # set turn field to team who plays first (always X)
            self.__turn__ = Team.X


    def move(self, row, col):
        '''
        Take turn as current team in specified position.

        Parameters
            row: int, row in which to play piece
            col: int, column in which to play piece

        Return
            new Board with move 

        '''
        # raise exception for invalid move
        self.check_bounds(row, col)
        if self.__spaces__[row][col]:
            raise Exception('Space already occupied!')

        # proceed with move by making copy and updating fields
        copy = Board(self)
        copy.__spaces__[row][col] = self.__turn__
        copy.__turn__ = Team.next(self.__turn__)
        return copy


    def get(self, row, col):
        '''
        Get piece in current space

        Parameters
            row: int, row check
            col: int, column to check

        Return
            int, Team.X, Team.O, or Team.NEITHER

        '''
        self.check_bounds(row, col)
        return self.__spaces__[row][col]

    def turn(self):
        '''
        Return
            int, Team who will play next
        '''
        return self.__turn__


    def check_bounds(self, row, col):
        '''
        Throw exception if value is out of bounds of this board.

        Parameters
            row: int, row to check
            col: int, column to check

        '''
        # raise exception for out-of-range input
        if row < 0 or row >= len(self.__spaces__):
            raise Exception('Invalid value for row!')
        if col < 0 or col >= len(self.__spaces__):
            raise Exception('Invalid value for column!')
