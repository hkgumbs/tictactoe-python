'''Define cpu behvior and interactions for simulation.'''

from models import Team, Board
from messages import CONFIRM, STATIC, UTIL

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
            return self._minimax(board, board.turn(), 0)[1]


class Simulation:
    '''
    Handle IO logic for simulation.
    '''

    def __init__(self):
        self._solver = Solver()
        self._board = Board()

    def get_teams(self):
        '''
        Prompt user which team they want to be and return assignments.

        Return
            Team constant, human team, Team.FIRST or Team.SECOND
            Team constant, cpu team

        '''
        while True:
            # use loop and try to catch ctrl-d and ctrl-c and retry input
            try:
                if raw_input(UTIL['team_prompt']) in CONFIRM:
                    return Team.FIRST, Team.SECOND
                else:
                    return Team.SECOND, Team.FIRST
            except (EOFError, KeyboardInterrupt):
                pass


    def check_game_over(self, board, solver):
        '''
        Check whether game is over and prompt user to retry if it is.

        Return
            bool, whether simulation should quit
            bool, whether simulation should restart

        '''
        winner = board.winner()
        if winner or not board.get(Team.NEITHER):
            # if game over

            print board

            if winner:
                print UTIL['lose_game']
            else:
                print UTIL['tie_game']

            confirm = raw_input(UTIL['retry_prompt'])
            if confirm in CONFIRM:
                quit = False
                restart = True
            else:
                quit = True
                restart = False  # doesn't matter

        else:
            quit = False
            restart = False

        return quit, restart
        

    def start(self):
        '''
        Control and loop game indefinitely until user quits, yielding output
        as it occurs.
        '''
        # initialize new game board and solver
        board = Board()
        solver = Solver()

        # yield instructions
        yield '\n%s\n' % STATIC['man']

        # initialize who goes first
        human, cpu = self.get_teams()

        # yield empty board
        yield board

        while True:

            if board.turn() == cpu:
                # if computer player's turn, make move
                move = solver.get_next_move(board)
                board = board.move(move)

                # yield computer move in (x,y) format
                yield ' %s >>> %d,%d' % (
                    Team.string(cpu), move % 3, move / 3)

                quit, restart = self.check_game_over(board, solver)
                if quit:
                    return
                elif restart:
                    board = Board()
                    human, cpu = self.get_teams()

                yield board

            else:
                try:
                    # request user input, remove whitespace, then parse
                    command = raw_input(' %s >>> ' % Team.string(board.turn()))
                    command = command.replace(' ', '')
                    
                    if command in STATIC:
                        yield STATIC[command]

                    elif command == 'undo':
                        if human in board:
                            # if human player has any pieces on board then undo
                            # twice since CPU had last move
                            board = board.undo().undo()
                            yield board

                        else: yield UTIL['undo_error']

                    elif command == 'print':
                        yield board

                    elif command == 'reset':
                        confirm = raw_input(UTIL['reset_confirm'])
                        if confirm in CONFIRM:
                            board = Board()
                            human, cpu = self.get_teams()
                            yield board

                    elif command == 'exit':
                        confirm = raw_input(UTIL['exit_confirm'])
                        if confirm in CONFIRM:
                            return

                    else:
                        # default case is integer indicies
                        try:
                            inds = [int(i) for i in command.split(',')]
                            if len(inds) not in [1, 2]:
                                # raise exception if input formatted incorrectly
                                raise ValueError
                            elif len(inds) == 2:
                                # user inputed coordinate as x and y
                                move = inds[1] * Board.SIZE + inds[0]
                            else:
                                # user inputed raw coordinate
                                # This option is not documented in the game
                                # instructions because it is mainly for testing.
                                move = inds[0]

                            board = board.move(move)
                            quit, restart = self.check_game_over(board, solver)
                            if quit:
                                return
                            elif restart:
                                board = Board()
                                human, cpu = self.get_teams()

                            yield board

                        except IndexError:
                            # move is out of bounds
                            yield UTIL['index_error']

                        except LookupError:
                            # space is already occupied
                            yield UTIL['lookup_error']

                        except ValueError:
                            # not an integer or improper format
                            yield UTIL['input_error']
                
                except KeyboardInterrupt:
                    # catch ctrl-c from user
                    yield UTIL['keyboard_interrupt']

                except EOFError:
                    # catch ctrl-d from user and exit gracefully
                    # undocumented because it provides no exit confirmation
                    return
