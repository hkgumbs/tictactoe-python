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

    @staticmethod
    def next(team):
        '''
        Given a valid team, this method will return the opposite team.

        Parameters
            team: int, either Team.X or Team.O

        Return
            opposite of team

        '''
        return Team.X + Team.O - team


    @staticmethod
    def get_string(team):
        '''
        Parameters
            team: int, valid Team constant

        Return
            str, representation of team as one-character string

        '''
        if team == Team.X: return 'X'
        elif team == Team.O: return 'O'
        else: return ' '


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

        if predecessor and move:
            self.__spaces__ = list(predecessor.__spaces__)  # copy list
            self.__spaces__[move] = predecessor.__turn__
            self.__turn__ = Team.next(predecessor.__turn__)
            self.__last__ = predecessor

        else:
            # board starts with (size * size) empty spaces, belonging to
            # neither team
            self.__spaces__ = [Team.NEITHER for _ in range(Board.SIZE ** 2)]

            # set turn field to team who plays first (always X)
            self.__turn__ = Team.X

            # empty board is its own predecessor, so undo is circular
            self.__last__ = self


    def __iter__(self):
        '''
        Return
            iter, iterator representing values of pieces on board.
        '''
        return iter(self.__spaces__)


    def __len__(self):
        '''
        Return
            int, number of spaces on board
        '''
        return len(self.__spaces__)


    def __str__(self):
        '''
        Return
            str, board in printable format.
        '''
        to_print = tuple([Team.get_string(space) for space in self.__spaces__])
        return '\n'.join([
            '     0   1   2',
            '  0  %s | %s | %s ',
            '    -----------',
            '  1  %s | %s | %s ',
            '    -----------',
            '  2  %s | %s | %s ',
            ''
        ]) % to_print


    def move(self, ind):
        '''
        Take turn as current team in specified position.

        Parameters
            ind: int, index of where to play piece, [0,9)

        Return
            new Board with move

        Throw
            Exception, when ind is out of bounds

        '''
        # raise exception for invalid move
        if ind < 0 or ind >= Board.SIZE ** 2:
            raise IndexError()
        if self.__spaces__[ind]:
            raise LookupError()

        # proceed with move by making copy for move
        return Board(predecessor=self, move=ind)


    def get(self, ind):
        '''
        Get piece in current space

        Parameters
            ind: int, index of space [0,9)

        Return
            int, Team.X, Team.O, or Team.NEITHER

        Throw
            Exception, when ind is out of bounds

        '''
        if ind < 0 or ind >= Board.SIZE ** 2:
            raise IndexError()
        return self.__spaces__[ind]


    def turn(self):
        '''
        Return
            int, Team who will play next

        '''
        return self.__turn__


    def undo(self):
        '''
        Return
            Board, board with state before last move or itself if board is
                empty

        '''
        return self.__last__


    def available(self):
        '''
        Return
            int, number of available spaces on board

        '''
        return len([None for space in self if space == Team.NEITHER])
