'''Define cpu behvior and interactions for simulation.'''

from models import Team, Board
import messages

class Solver:
    '''Define AI logic for cpu player.'''

    def _minimax(self, board, cpu, depth):
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
        winner = board.winner()
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
            scores = [(self._minimax(
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
            _, move = self._minimax(board, board.turn(), 0)
            return move


class Simulation:
    '''
    Handle IO logic for simulation.
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
        Gets input from user while applying given constraints

        Paramaters
            prompt: str, message to guide user
            restrictions: str[], list of valid input options

        Return
            str, input from user

        '''
        while True:
            result = raw_input(prompt)
            if result in restrictions:
                return result
            else:
                print messages.UTIL['input_error']
    

    def __init__(self):
        self._state = Simulation.INIT
        self._solver = Solver()
        self.board = Board()


    def has_next(self):
        '''
        Return
            True if simulation is ongoing, False otherwise
        '''
        return self._state != FINISHED


    def next(self):
        if self._state == Simulation.INIT:
            # game has just started, so print out rules
            result = '\n%s\n' % STATIC['man']
            self._state == Simulation.PROMPT_TEAM

        elif self._state == Simulation.PROMPT_TEAM:
            # ask user is they would like to go first
            choice = Simulation.get_input(
                messages.UTIL['team_prompt'], messages.BINARY)
            if choice in messages.YES:
                self._state = Simulation.PLAYER_MOVE
            else:
                self._state = Simulation.CPU_MOVE
            result = self._board

        elif self._state == Simulation.CPU_MOVE:
            # if computer player's turn, make move
            move = solver.get_next_move(board)
            board = board.move(move)

            # result is cpu move and string representation of board
            result_list = [' %s >>> %d' % move, str(board)]

            # if game is over, append game over message
            if board.game_over():
                result_list.append(messages.UTIL['lose_game'] \
                    if board.winner() else messages.UTIL['tie_game'])
                self._state = Simulation.PROMPT_RESTART
            else:
                self._state = Simulation.PLAYER_MOVE

            result = '\n'.join(result_list)

        elif self._state == Simulation.PLAYER_MOVE:
            # commands include available spaces, an action, or a help command
            options = [str(x) for x in self._board.get(Team.NEITHER)] + \
                messages.ACTIONS + messages.STATIC.keys()
            prompt = '%s >>> ' % Team.string(board.turn())
            command = Simulation.get_input(prompt, options)
            
            if command in messages.STATIC:
                # print help message
                result = messages.STATIC[command]

            elif command == 'undo':
                if board.turn() in board:
                    # check that player has a move that can be undone
                    # undo twice to undo cpu's move as well
                    self._board = self._board.undo().undo()
                    result = str(board)
                else:
                    result = UTIL['undo_error']

            elif command == 'print':
                result = str(board)

            elif command == 'quit':
                result = ''  # return empty line to print
                self._state = Simulation.PROMPT_RESTART

            else:  # integer coordinate
                self._board = self._board.move(command)
                self._state = Simulation.CPU_MOVE
                result = str(board)

        elif self._state == Simulation.PROMPT_RESTART:
            # ask whether player wants to play again
            choice = Simulation.get_input(
                messages.UTIL['retry_prompt'], messages.BINARY)
            if choice in messages.YES:
                self._board = Board()
                self._state = Simulation.PROMPT_TEAM
            else:
                self._state = Simulation.FINISHED

        return result
