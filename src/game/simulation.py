from game.board import Board
from game.solver import Solver
from game.team import Team
from game import static


class Simulation:
    '''
    Handle IO logic for simulation. Simulation objects function as iterable
    finite state machines.
    '''

    # State variables
    INIT = 0
    PROMPT_TEAM = 1
    PLAYER_MOVE = 2
    CPU_MOVE = 3
    PROMPT_RESTART = 4
    FINISHED = 5

    @staticmethod
    def get_input(prompt, restrictions):
        '''
        Get input from user while applying given constraints

        Parameters
            prompt: str, message to guide user
            restrictions: str[], list of valid input options

        Return
            str, input from user

        '''
        # keep requesting until valid input received
        while True:
            result = input(prompt)
            if result in restrictions:
                return result
            else:
                print(static.UTIL['input_error'])

    def __init__(self):
        '''
        Initialize fieleds.

        '''
        self._solver = Solver()
        self._board = Board()
        self._state = Simulation.INIT

    def __iter__(self):
        '''
        Mark Simulation objects as iterable

        Return
            Simulation, this object

        '''
        return self

    def __next__(self):
        '''
        Continue simulation until next piece of output is available

        Return
            str, output from game since last call to next()

        '''
        if self._state == Simulation.INIT:
            return self._state_init()

        elif self._state == Simulation.PROMPT_TEAM:
            return self._state_prompt_team()

        elif self._state == Simulation.CPU_MOVE:
            return self._state_cpu_move()

        elif self._state == Simulation.PLAYER_MOVE:
            return self._state_player_move()

        elif self._state == Simulation.PROMPT_RESTART:
            return self._state_prompt_restart()

        else:  # self._state == Simulation.FINISHED
            raise StopIteration

    def _state_init(self):
        '''
        Update state to PROMPT_TEAM

        Return
            str, rules for simulation

        '''
        self._state = Simulation.PROMPT_TEAM
        return '\n%s\n' % static.INFO['man']

    def _state_prompt_team(self):
        '''
        Determine teams and update state to either CPU_MOVE or PLAYER_MOVE

        Return
            str, board representation

        '''
        # ask user is they would like to go first
        choice = Simulation.get_input(
            static.UTIL['team_prompt'], static.BINARY)
        if choice in static.YES:
            self._state = Simulation.PLAYER_MOVE
        else:
            self._state = Simulation.CPU_MOVE

        return str(self._board)

    def _state_cpu_move(self):
        '''
        Make cpu move and update state to either PROMPT_RESTART or
        PLAYER_MOVE

        Return
            str, board representation and optional end of game message

        '''
        move = self._solver.get_next_move(self._board)
        turn = str(self._board.turn())
        self._board = self._board.move(move)

        # result is cpu move and string representation of board
        result = ['%s >>> %d' % (turn, move), str(self._board)]

        # if game is over, append game over message
        if self._board.game_over():
            result.append(static.UTIL['lose_game']
                          if self._board.winner() else static.UTIL['tie_game'])
            self._state = Simulation.PROMPT_RESTART
        else:
            self._state = Simulation.PLAYER_MOVE

        return '\n'.join(result)

    def _state_player_move(self):
        '''
        Request player move and update state to either PROMPT_RESTART or
        PLAYER_MOVE

        Return
            str, board representation and optional end of game message

        '''
        # commands include available spaces, an action, or a help command
        options = [str(x) for x in self._board.get(Team.NEITHER)] + \
            static.ACTIONS + list(static.INFO.keys())
        prompt = '%s >>> ' % str(self._board.turn())
        command = Simulation.get_input(prompt, options)

        if command in static.INFO:
            # print help message
            return static.INFO[command]

        elif command == 'undo':
            if self._board.turn() in self._board:
                # check that player has a move that can be undone
                # undo twice to undo cpu's move as well
                self._board = self._board.undo().undo()
                return str(self._board)
            else:
                return static.UTIL['undo_error']

        elif command == 'print':
            return str(self._board)

        elif command == 'quit':
            self._state = Simulation.PROMPT_RESTART
            return ''  # return empty line to print

        else:  # integer coordinate
            self._board = self._board.move(int(command))
            result = [str(self._board)]

            # if game is over, append game over message
            if self._board.game_over():
                result.append(static.UTIL['tie_game'])
                self._state = Simulation.PROMPT_RESTART
            else:
                self._state = Simulation.CPU_MOVE

            return '\n'.join(result)

    def _state_prompt_restart(self):
        '''
        Determine whether to re-run simulation and update state to either
        PROMPT_TEAM of FINISHED

        Return
            str, board representation

        '''
        # ask whether player wants to play again
        choice = Simulation.get_input(
            static.UTIL['retry_prompt'], static.BINARY)
        if choice in static.YES:
            self._board = Board()
            self._state = Simulation.PROMPT_TEAM
        else:
            self._state = Simulation.FINISHED

        return ''  # return empty line to print

    def board(self):
        '''
        Return
            Board, current board for this simulation

        '''
        return self._board

    def state(self):
        '''
        Return
            int, current Simulation state constant for this simulation

        '''
        return self._state
