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
            scores = [(self._minimax(board.move(i), cpu, depth + 1)[0], i) \
                    for i in board.get(Team.NEITHER)]
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
    '''Handle IO logic for simulation.'''

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
        # keep requesting until valid input received
        while True:
            result = raw_input(prompt)
            if result in restrictions:
                return result
            else:
                print messages.UTIL['input_error']
    

    def __init__(self):
        self._solver = Solver()
        self.board = Board()
        self.state = Simulation.INIT


    def has_next(self):
        '''
        Return
            True if simulation is ongoing, False otherwise

        '''
        return self.state != Simulation.FINISHED


    def next(self):
        '''
        Continues simulation until next piece of output is available

        Return
            str, output from game since last call to next()

        '''
        if self.state == Simulation.INIT:
            return self.state_init()

        elif self.state == Simulation.PROMPT_TEAM:
            return self.state_prompt_team()            

        elif self.state == Simulation.CPU_MOVE:
            self.state_cpu_move()

        elif self.state == Simulation.PLAYER_MOVE:
            self.state_player_move()

        elif self.state == Simulation.PROMPT_RESTART:
            self._state_prompt_restart()

        else:  # unknown state reached
            raise ValueError()


    def state_init(self):
        '''
        Updates state to PROMPT_TEAM

        Return
            str, rules for simulation
        '''
        self.state = Simulation.PROMPT_TEAM
        return '\n%s\n' % messages.STATIC['man']


    def state_prompt_team(self):
        '''
        Determines teams and updates state to either CPU_MOVE or PLAYER_MOVE

        Return
            str, board representation

        '''
        # ask user is they would like to go first
        choice = Simulation.get_input(
                messages.UTIL['team_prompt'], messages.BINARY)
        if choice in messages.YES:
            self.state = Simulation.PLAYER_MOVE
        else:
            self.state = Simulation.CPU_MOVE

        return str(self.board)


    def state_cpu_move(self):
        '''
        Makes cpu move and updates state to either PROMPT_RESTART or
        PLAYER_MOVE

        Return
            str, board representation and optional end of game message

        '''
        move = self._solver.get_next_move(self.board)
        turn = Team.string(self.board.turn())
        self.board = self.board.move(move)

        # result is cpu move and string representation of board
        result_list = ['%s >>> %d' % (turn, move), str(self.board)]

        # if game is over, append game over message
        if self.board.game_over():
            result_list.append(messages.UTIL['lose_game'] \
                    if self.board.winner() else messages.UTIL['tie_game'])
            self.state = Simulation.PROMPT_RESTART
        else:
            self.state = Simulation.PLAYER_MOVE

        return '\n'.join(result_list)


    def state_player_move(self):
        '''
        Request player move and updates state to either PROMPT_RESTART or
        PLAYER_MOVE

        Return
            str, board representation and optional end of game message

        '''
        # commands include available spaces, an action, or a help command
        options = [str(x) for x in self.board.get(Team.NEITHER)] + \
                messages.ACTIONS + messages.STATIC.keys()
        prompt = '%s >>> ' % Team.string(self.board.turn())
        command = Simulation.get_input(prompt, options)
        
        if command in messages.STATIC:
            # print help message
            return messages.STATIC[command]

        elif command == 'undo':
            if self.board.turn() in self.board:
                # check that player has a move that can be undone
                # undo twice to undo cpu's move as well
                self.board = self.board.undo().undo()
                return str(self.board)
            else:
                return messages.UTIL['undo_error']

        elif command == 'print':
            return str(self.board)

        elif command == 'quit':
            self.state = Simulation.PROMPT_RESTART
            return ''  # return empty line to print

        else:  # integer coordinate
            self.board = self.board.move(int(command))
            result_list = [str(self.board)]

            # if game is over, append game over message
            if self.board.game_over():
                result_list.append(messages.UTIL['tie_game'])
                self.state = Simulation.PROMPT_RESTART
            else:
                self.state = Simulation.CPU_MOVE

            return '\n'.join(result_list)


    def state_prompt_restart(self):
        # ask whether player wants to play again
        choice = Simulation.get_input(
            messages.UTIL['retry_prompt'], messages.BINARY)
        if choice in messages.YES:
            self.board = Board()
            self.state = Simulation.PROMPT_TEAM
        else:
            self.state = Simulation.FINISHED

        return ''  # return empty line to print
