'''Tests for tic tac toe solver.'''

from models import Board, Team
from simulation import Solver, Simulation
import unittest

class TestSolver():

    def test_naive(self):
        '''
        Test that cpu always defeats a naive player who always takes first
        available space. Functioned as basic sanity test during production.
        '''
        for cpu in [Team.FIRST, Team.SECOND]:
            # perform test with cpu as both first and second player

            board = Board()
            solver = Solver()
            while not board.game_over():
                # play until winner is determined

                if cpu == board.turn():
                    board = board.move(solver.get_next_move(board))

                else:
                    # play move on first available space
                    board = board.move(board.get(Team.NEITHER)[0])

            # cpu should always win
            print board
            assert board.winner() == cpu


    def test_two_cpus(self):
        '''Test that two cpu players should always end games in a draw.'''
        board = Board()
        solver = Solver()
        while board.get(Team.NEITHER):
            # always play the best calculated move
            board = board.move(solver.get_next_move(board))

        # board should end with no winner
        assert not board.winner()


    # def test_never_lose(self):
    #     '''Test that cpu player never loses a match.'''
    #     for cpu in [Team.FIRST, Team.SECOND]:
    #         # perform test with cpu as both first and second player
    #         _never_lose(Board(), Solver(), cpu)


    def _never_lose(self, board, solver, cpu):
        '''
        Recursively descend into every possible game state to determin that 
        cpu player never loses.

        Parameters
            board: Board, board to assess
            cpu: Team, cpu team
        '''
        winner = board.winner()
        if winner == cpu:
            # base case, cpu wins
            return

        elif winner:
            # base case, human wins, should never occur 
            assert False

        elif board.get(Team.NEITHER):
            if board.turn() == cpu:
                _never_lose(board.move(solver.get_next_move(board)), solver, cpu)
            else:
                for space in board.get(Team.NEITHER):
                    # make every possible move
                    _never_lose(board.move(space), solver, cpu)

        # else tie game

if __name__ == '__main__':
    TestSolver().test_naive()
    # unittest.main()
