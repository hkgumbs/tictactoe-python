'''Tests for tic tac toe solver.'''

from models import Board, Team
from controllers import Solver, Simulation
import unittest

class TestModels(unittest.TestCase):

    def test_team(self):
        '''Test basic Team object identities functions'''
        assert Team.FIRST != Team.SECOND
        assert not Team.NEITHER
        assert Team.FIRST.other() == Team.SECOND
        assert Team.SECOND.other() == Team.FIRST


    def test_board(self):
        '''Test basic board functionality'''
        board = Board()
        self._board_get_assert(board, 0, 0, len(board))

        board = board.move(0)
        self._board_get_assert(board, 1, 0, len(board) - 1)

        board = board.undo()
        self._board_get_assert(board, 0, 0, len(board))


    def _board_get_assert(self, board, num_first, num_second,  num_neither):
        '''
        Asserts whether board has the appropriate number of pieces

        Parameters
            board: Board
            num_first: int, number of spaces Team.FIRST should occupy
            num_second: int, number of spaces Team.SECOND should occupy
            num_neither: int, number of spaces Team.NEITHER should occupy
        '''
        assert len(board.get(Team.NEITHER)) == num_neither
        assert len(board.get(Team.FIRST)) == num_first
        assert len(board.get(Team.SECOND)) == num_second


class TestSolver(unittest.TestCase):

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


    def test_never_lose(self):
        '''Test that cpu player never loses a match.'''
        for cpu in [Team.FIRST, Team.SECOND]:
            # perform test with cpu as both first and second player
            self._never_lose(Board(), Solver(), cpu)


    def _never_lose(self, board, solver, cpu):
        '''
        Recursively descend into every possible game state to determine that
        cpu never loses.

        Parameters
            board: Board, board to assess
            cpu: Team, cpu team
        '''
        if board.game_over():
            winner = board.winner()
            if winner == cpu:
                # base case, cpu wins
                return

            elif winner:
                # base case, human wins, should never occur 
                assert False

        elif board.get(Team.NEITHER):
            if board.turn() == cpu:
                self._never_lose(
                        board.move(solver.get_next_move(board)), solver, cpu)
            else:
                for space in board.get(Team.NEITHER):
                    # make every possible move
                    self._never_lose(board.move(space), solver, cpu)

        # else tie game


class TestSimulation(unittest.TestCase):

    def test_dummy(self):
        pass

if __name__ == '__main__':
    unittest.main()
