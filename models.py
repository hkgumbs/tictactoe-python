'''
Defines the game board, which is a 3-by-3 square for exactly 2 teams.
'''

class Team:
    '''
    Constants that represent the different valid states of a space or turn.
    NEITHER is garunteed to evaluate to False.
    '''
    NEITHER = 0
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
    Encapsulation of spaces and board state. This class is effectively
    immutable to make recursive operations more intuitive. The Board object
    keeps track of which team will make the next move, but it is unaware of
    conditions for victory. Therefore, a Board object cannot tell if the game
    is over or who has won.
    '''
    SIZE = 3

    def __init__(self, copy=None):
        '''
        Initialize board spaces and current turn state.

        Parameters
            copy: Board, board to copy

        '''

        if copy:
            self.__spaces__ = list(copy.__spaces__)  # copy list
            self.__turn__ = copy.__turn__

        else:
            # board starts with (size * size) empty spaces, belonging to
            # neither team
            self.__spaces__ = [Team.NEITHER for _ in range(Board.SIZE) ** 2]

            # set turn field to team who plays first (always X)
            self.__turn__ = Team.X


    def __str__(self):
        '''
        Return
            str, board in printable format.
        '''
        return '\n'.join([
            ' %s | %s | %s ',
            '-----------',
            ' %s | %s | %s ',
            '-----------',
            ' %s | %s | %s '
        ]) % tuple(self.__spaces__)


    def move(self, ind):
        '''
        Take turn as current team in specified position.

        Parameters
            ind: int, index of where to play piece, [0,9)

        Return
            new Board with move 

        '''
        # raise exception for invalid move
        if ind < 0 or ind >= Board.SIZE ** 2:
            raise Exception('Invalid index value!')
        if self.__spaces__[ind]:
            raise Exception('Space already occupied!')

        # proceed with move by making copy and updating fields
        copy = Board(self)
        copy.__spaces__[ind] = self.__turn__
        copy.__turn__ = Team.next(self.__turn__)
        return copy


    def get(self, ind):
        '''
        Get piece in current space

        Parameters
            ind: int, index of space [0,9)

        Return
            int, Team.X, Team.O, or Team.NEITHER

        '''
        if ind < 0 or ind >= Board.SIZE ** 2:
            raise Exception('Invalid index value!')
        return self.__spaces__[ind]


    def turn(self):
        '''
        Return
            int, Team who will play next

        '''
        return self.__turn__
