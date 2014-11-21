'''Tests for tic tac toe solver.'''

from models import Board, Team
from controllers import Solver, Simulation
import unittest
import sys

class TestModels(unittest.TestCase):

    def test_team(self):
        '''Test basic Team object identities functions'''
        assert Team.FIRST != Team.SECOND
        assert not Team.NEITHER
        assert Team.FIRST.other() == Team.SECOND
        assert Team.SECOND.other() == Team.FIRST

        # test unique hashes
        h = {}
        h[Team.FIRST] = True
        h[Team.SECOND] = True
        h[Team.NEITHER] = True
        assert len(h) == 3


    def test_board(self):
        '''Test basic board functionality'''
        board = Board()
        self._board_state_assert(board, 0, 0)

        board = board.move(0)
        self._board_state_assert(board, 1, 0)

        board = board.undo()
        self._board_state_assert(board, 0, 0)

        # tie game
        board = Board()
        moves = [0, 1, 4, 2, 5, 3, 6, 8, 7]
        for move in moves:
            board = board.move(move)
        self._board_state_assert(board, 5, 4, over=True)

        # put Team.FIRST in a winning state
        board = Board()
        moves = [0, 3, 1, 4, 2]
        for move in moves:
            board = board.move(move)
        board = Board().move(0).move(3).move(1).move(4).move(2)
        self._board_state_assert(board, 3, 2, over=True, winner=Team.FIRST)

        board = board.undo()
        self._board_state_assert(board, 2, 2)
        assert board.turn() == Team.FIRST


    def _board_state_assert(self, board, num_first, num_second, 
            over=False, winner=Team.NEITHER):
        '''
        Asserts whether board has the appropriate number of pieces

        Parameters
            board: Board
            num_first: int, number of spaces Team.FIRST should occupy
            num_second: int, number of spaces Team.SECOND should occupy
        '''
        assert len(board.get(Team.FIRST)) == num_first
        assert len(board.get(Team.SECOND)) == num_second
        assert len(board.get(Team.NEITHER)) == len(board) - \
                num_first - num_second
        assert board.game_over() == over
        assert board.winner() == winner


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


    def _test_two_cpus(self):  # TODO
        '''Test that two cpu players should always end games in a draw.'''
        board = Board()
        solver = Solver()
        while board.get(Team.NEITHER):
            # always play the best calculated move
            board = board.move(solver.get_next_move(board))

        # board should end with no winner
        assert not board.winner()


    def _test_never_lose(self):  # TODO
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

        else:
            if board.turn() == cpu:
                self._never_lose(
                        board.move(solver.get_next_move(board)), solver, cpu)
            else:
                for space in board.get(Team.NEITHER):
                    # make every possible move
                    self._never_lose(board.move(space), solver, cpu)

        # else tie game


class TestSimulation(unittest.TestCase):

    def test_one_move(self):
        with open('test_input.txt', 'w+') as test_input:
            lines = [
                    'y\n',  # yes to play first
                    '0\n'  # play in the first position
            ]
            for line in lines:
                test_input.write(line)
            test_input.seek(0)
            sys.stdin = test_input

            sim = Simulation()
            assert sim.state() == Simulation.INIT

            sim.next()
            assert sim.state() == Simulation.PROMPT_TEAM

            sim.next()
            assert sim.state() == Simulation.PLAYER_MOVE

            sim.next()
            assert sim.state() == Simulation.CPU_MOVE

            assert len(sim.board().get(Team.FIRST)) == 1
            assert len(sim.board().get(Team.SECOND)) == 0
            assert sim.board().turn() == Team.SECOND

if __name__ == '__main__':
    unittest.main()
