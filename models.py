'''Model classes defining the unbeatable tic-tac-toe game.'''

class Team:
    '''
    Constants that represent the different valid states of a space or turn.
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
    '''Encapsulation of spaces and board state.'''

    def __init__(self, plays_first=Team.X):
        '''
        Initialize board spaces and current turn state.

        Parameters
            plays_first: int, which team (X or O) should play first

        '''

        # board starts with all empty spaces, belonging to neither team
        self.spaces = [
            [Team.NEITHER, Team.NEITHER, Team.NEITHER],
            [Team.NEITHER, Team.NEITHER, Team.NEITHER],
            [Team.NEITHER, Team.NEITHER, Team.NEITHER]
        ]

        # set turn field to team who plays first
        self.turn = Team.X if plays_first == Team.X else Team.O


    def move(self, row, col):
        '''
        Take turn as current team in specified position.

        Parameters
            row: int, row in which to play piece
            col: int, column in which to play piece

        '''

        # bound row and column to valid values
        if row < 0: row = 0
        elif row > 2: row = 2
        if col < 0: col = 0
        elif col > 2: col = 2

        # mark space with current team
        self.spaces[row][col] = self.turn

        # toggle turn field
        self.turn = Team.next(self.turn)

