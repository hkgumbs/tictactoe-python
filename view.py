'''
Handle IO for tic-tac-toe game.
'''

from models import Board

def main():
    '''
    Control and loop game indefeinitely until user quits.
    '''
    print 'Welcome to un anbeatable tic-tac-toe game!'
    print '\n'

    board = Board()
    next_move = None
    count = 0
    while not next_move:
        print board, '\n'
        try:
            next_move = int(raw_input())
            board.move(next_move)
            count += 1
            if count > 9:
                break
        except:
            next_move = None


if __name__ == '__main':
    main()
