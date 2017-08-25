from game.team import Team


class Solver:
    '''Define AI logic for cpu player.'''

    def _minimax(self, board, cpu, depth):
        '''
        Scores game state and determines best move for the next play.

        Parameters
            board: Board, board to assess
            cpu: Team, cpu team
            depth: number of recurses into future states

        Return
            int, score
            int, best move or -1 if game is over

        '''
        if board.game_over():
            winner = board.winner()
            if winner == cpu:
                return 10 - depth, -1
            elif winner == Team.NEITHER:
                # tie game
                return 0, -1
            else:  # player won
                return depth - 10, -1

        else:
            scores = [(self._minimax(board.move(i), cpu, depth + 1)[0], i)
                      for i in board.get(Team.NEITHER)]
            if board.turn() == cpu:
                return max(scores)
            else:
                return min(scores)

    def get_next_move(self, board):
        '''
        Suggest next move according to minimax algorithm. Board must represent an
        ongoing game.

        Parameters
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
