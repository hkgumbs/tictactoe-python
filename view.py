'''
Handle IO for tic-tac-toe game.
'''

from ai import get_winner
from messages import instructions, help
from models import Board

def main():
    '''
    Control and loop game indefinitely until user quits.
    '''
    # print instructions to terminal
    print instructions

    # initialize board and game status
    board = Board()
    num_moves = 0
    game_ongoing = True

    while game_ongoing:
        print board
        try:
            # TODO
            next_move = int(raw_input('>>> '))
            board = board.move(next_move)
            num_moves += 1

            # TODO
            winner = get_winner(board)
            spaces_remaining = num_moves < Board.SIZE ** 2
            game_ongoing = not winner and spaces_remaining
        
        except Exception, e:
            # TODO
            print e
            print help

        # print new line for readability
        print ''


if __name__ == '__main__':
    main()
