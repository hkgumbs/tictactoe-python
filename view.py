'''
Handle IO for tic-tac-toe game.
'''

from ai import get_winner
from messages import UTIL, STATIC
from models import Board, Team
import re

def main():
    '''
    Control and loop game indefinitely until user quits. This 
    '''
    # print instructions to terminal
    print '\n%s\n' % STATIC['man']

    # initialize board and game status
    board = Board()
    game_ongoing = True
    human = Team.X

    while game_ongoing:

        # show current board
        print board

        # if computer player's turn, make move
        # TODO

        # request user input and remove whitespace
        command = raw_input(' %s >>> ' % Team.get_string(board.turn()))
        command = command.strip().replace(' ', '')

        try:
            # parse command

            if command in STATIC:
                print STATIC[command]

            elif command == 'undo':
                if human in board:
                    # if human player has any pieces on board then undo twice
                    # since CPU had last move
                    board = board.undo().undo()

                else: print UTIL['undo_error']

            elif command == 'reset':
                # TODO
                pass

            elif command == 'exit':
                return

            else:
                # default case is integer indicies

                m = re.match(r'(\d+)(,\d+)?', command)
                if m:
                    if m.group(1) is not None:
                        # user inputed coordinate as row and column
                        move = int(m.group(0)) * Board.SIZE + \
                            int(m.group(1).replace(',', ''))
                    
                    else:
                        # user inputed raw coordinate
                        # This option is not documented in the game
                        # instructions because it is mainly for testing.
                        move = int(m.group(0))
                    
                    try:
                        board = board.move(move)
                        winner = get_winner(board)
                        spaces_remaining = board.available() > 0
                        game_ongoing = not winner and spaces_remaining

                    except IndexError:
                        # move is out of bounds
                        print UTIL['index_error']

                    except LookupError:
                        # space is already occupied
                        print UTIL['lookup_error']

                else: print UTIL['input_error']
        
        except KeyboardInterrupt:
            # catch ctrl-c from user
            print UTIL['keyboard_interrupt']

        # print new line for readability
        print '\n ----------------- \n'


if __name__ == '__main__':
    main()
