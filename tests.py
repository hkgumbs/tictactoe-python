'''Tests for tic tac toe solver.'''

import src
from src.board import Board
from src.team import Team
from src.solver import Solver
from src.simulation import Simulation
import unittest
import sys

class BaseTest(unittest.TestCase):
    '''Abstract test class'''

    def board_state_assert(self, board, num_first, num_second,
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
        assert board.turn() == Team.FIRST \
                if num_first == num_second else Team.SECOND


class TestModels(BaseTest):

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
        self.board_state_assert(board, 0, 0)

        board = board.move(0)
        self.board_state_assert(board, 1, 0)

        board = board.undo()
        self.board_state_assert(board, 0, 0)

        # tie game
        board = Board()
        moves = [0, 1, 4, 2, 5, 3, 6, 8, 7]
        for move in moves:
            board = board.move(move)
        self.board_state_assert(board, 5, 4, over=True)

        # put Team.FIRST in a winning state
        board = Board()
        moves = [0, 3, 1, 4, 2]
        for move in moves:
            board = board.move(move)
        board = Board().move(0).move(3).move(1).move(4).move(2)
        self.board_state_assert(board, 3, 2, over=True, winner=Team.FIRST)

        board = board.undo()
        self.board_state_assert(board, 2, 2)
        assert board.turn() == Team.FIRST


class TestSolver(BaseTest):

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


    def test_two_cpus(self):  # TODO
        '''Test that two cpu players should always end games in a draw.'''
        board = Board()
        solver = Solver()
        while board.get(Team.NEITHER):
            # always play the best calculated move
            board = board.move(solver.get_next_move(board))

        # board should end with no winner
        assert not board.winner()


    def test_never_lose(self):  # TODO
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


class TestSimulation(BaseTest):

    def test_first_moves(self):
        '''Test initial move states'''
        with open('test_input.txt', 'w+') as test_input:
            lines = [
                    'y\n',  # yes to play first
                    '0\n',  # play in the first position
                    'undo'  # undo previous move
            ]
            for line in lines:
                test_input.write(line)
            test_input.seek(0)
            sys.stdin = test_input

            sim = Simulation()
            assert sim.state() == Simulation.INIT

            next(sim)
            assert sim.state() == Simulation.PROMPT_TEAM

            next(sim)  # read y
            assert sim.state() == Simulation.PLAYER_MOVE

            next(sim)  # read 0
            assert sim.state() == Simulation.CPU_MOVE
            self.board_state_assert(sim.board(), 1, 0)

            next(sim)
            assert sim.state() == Simulation.PLAYER_MOVE
            self.board_state_assert(sim.board(), 1, 1)

            next(sim)  # read undo
            assert sim.state() == Simulation.PLAYER_MOVE
            self.board_state_assert(sim.board(), 0, 0)


    def test_extra_features(self):
        '''Test extra simulation commands'''
        with open('test_input.txt', 'w+') as test_input:
            lines = [
                    'y\n',  # yes to play first
                    'help\n',  # print extra commands
                    'man\n',  # print manual
                    'print\n',  # print board
                    'docs\n',  # print attribution
                    'quit\n',  # exit simulation
                    'n'  # confirm exit
            ]
            for line in lines:
                test_input.write(line)
            test_input.seek(0)
            sys.stdin = test_input

            sim = Simulation()
            assert sim.state() == Simulation.INIT

            next(sim)
            assert sim.state() == Simulation.PROMPT_TEAM

            next(sim)  # read y
            assert sim.state() == Simulation.PLAYER_MOVE

            next(sim)  # read help
            assert sim.state() == Simulation.PLAYER_MOVE

            next(sim)  # read man
            assert sim.state() == Simulation.PLAYER_MOVE

            next(sim)  # read print
            assert sim.state() == Simulation.PLAYER_MOVE

            next(sim)  # read docs
            assert sim.state() == Simulation.PLAYER_MOVE

            next(sim)  # read quit
            assert sim.state() == Simulation.PROMPT_RESTART

            next(sim)
            assert sim.state() == Simulation.FINISHED
            self.board_state_assert(sim.board(), 0, 0)


    def test_full_match(self):
        '''Test full match simulation'''
        with open('test_input.txt', 'w+') as test_input:
            lines = [
                    'n\n',  # no to play second
                    '2\n',  # play in the second position
                    '1\n',  # play to right of previous piece
                    'n'  # quit (assuming player has lost)
            ]
            for line in lines:
                test_input.write(line)
            test_input.seek(0)
            sys.stdin = test_input

            sim = Simulation()
            assert sim.state() == Simulation.INIT

            next(sim)
            assert sim.state() == Simulation.PROMPT_TEAM

            next(sim)  # read n
            assert sim.state() == Simulation.CPU_MOVE

            next(sim)
            assert sim.state() == Simulation.PLAYER_MOVE

            next(sim)  # read 2
            assert sim.state() == Simulation.CPU_MOVE

            next(sim)
            assert sim.state() == Simulation.PLAYER_MOVE

            next(sim)  # read 1
            assert sim.state() == Simulation.CPU_MOVE

            next(sim)
            assert sim.state() == Simulation.PROMPT_RESTART

            next(sim)
            assert sim.state() == Simulation.FINISHED
            self.board_state_assert(sim.board(), 3, 2, \
                    over=True, winner=Team.FIRST)


if __name__ == '__main__':
    with open('test_output.txt', 'w') as test_output:
        sys.stdout = test_output  # hide prompts and output from simulation
        unittest.main()
