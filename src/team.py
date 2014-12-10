class Team:
    '''
    Abstraction that encapsulates the different valid states of a space or
    turn. NEITHER is garunteed to evaluate to False. Team objects are
    immutable.
    '''

    # dictionary to associate opposing teams
    OTHER = {}

    def __init__(self, marker):
        '''
        Initialize team object representation.

        Parameters
            marker: str, how to represent team in string representation of
            board

        '''
        self._marker = marker


    def __str__(self):
        '''
        Return
            str, representation of team

        '''
        return self._marker


    def __eq__(self, obj):
        '''
        Return
            bool, True if two markers representthe same team, False otherwise

        '''
        return isinstance(obj, Team) and self._marker == obj._marker


    def __hash__(self):
        '''
        Return
            int, hash for object

        '''
        return hash(self._marker)


    def __nonzero__(self):
        '''
        Return
            bool, True if not Team.NEITHER, False otherwise

        '''
        return self != Team.NEITHER


    def other(self):
        '''
        Given a valid team, this method will return the opposite team.

        Parameters
            team: Team, either Team.FIRST or Team.SECOND

        Return
            Team, opposite of team

        '''
        return Team.OTHER[self]

# initialize team constants
Team.FIRST = Team('x')
Team.SECOND = Team('o')
Team.NEITHER = Team(' ')
Team.OTHER[Team.FIRST] = Team.SECOND
Team.OTHER[Team.SECOND] = Team.FIRST
