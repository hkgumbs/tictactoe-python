'''
Handle IO for tic-tac-toe game.
'''

from solver import get_winner, get_next_move
from messages import UTIL, STATIC
from models import Board, Team

def get_team():
    '''
    Prompt user which team they want to be and return that team.

    Return
        int, Team.FIRST or Team.SECOND

    '''
    if raw_input(UTIL['team_prompt']) == 'y':
        return Team.FIRST
    else:
        return Team.SECOND


def check_game_over(board):
    '''
    Check whether game is over and prompt user to retry if it is.

    Return
        bool, whether simulation should quit
        bool, whether simulation should restart

    '''
    winner = get_winner(board)
    spaces_remaining = board.available() > 0

    if winner or not winner and not spaces_remaining:
        # if game over
        print board
        if winner:
            print UTIL['lose_game']
        else:
            print UTIL['tie_game']

        confirm = raw_input(UTIL['retry_prompt'])
        if confirm == 'y':
            quit = False
            restart = True
        else:
            quit = True
            restart = False  # doesn't matter

    else:
        quit = False
        restart = False

    return quit, restart
    

def main():
    '''
    Control and loop game indefinitely until user quits. 
    '''
    # initialize new game board
    board = Board()

    # print instructions
    print '\n%s\n' % STATIC['man']

    # initialize who goes first
    try:
        human = get_team()
    except EOFError: return

    # print empty board
    print board

    while True:

        if board.turn() != human:
            # if computer player's turn, make move
            move = get_next_move(board)
            board = board.move(move)

            # print computer move in (row,col) format
            print ' %s >>> %d,%d' % (
                Team.get_string(Team.other(human)), move % 3, move / 3)

            quit, restart = check_game_over(board)
            if quit:
                return
            elif restart:
                board = Board()
                human = get_team()

            print board

        else:
            try:
                # request user input, remove whitespace, then parse
                command = raw_input(' %s >>> ' % Team.get_string(board.turn()))
                command = command.replace(' ', '')
                
                if command in STATIC:
                    print STATIC[command]

                elif command == 'undo':
                    if human in board:
                        # if human player has any pieces on board then undo
                        # twice since CPU had last move
                        board = board.undo().undo()

                    else: print UTIL['undo_error']

                elif command == 'print':
                    print board

                elif command == 'reset':
                    confirm = raw_input(UTIL['reset_confirm'])
                    if confirm == 'y':
                        board = Board()
                        human = get_team()
                        print board

                elif command == 'exit':
                    try:
                        confirm = raw_input(UTIL['exit_confirm'])
                        if confirm == 'y': return
                    except: pass

                else:
                    # default case is integer indicies
                    try:
                        inds = [int(i) for i in command.split(',')]
                        if len(inds) not in [1, 2]:
                            # raise exception if input formatted incorrectly
                            raise ValueError
                        elif len(inds) == 2:
                            # user inputed coordinate as row and column
                            move = inds[0] * Board.SIZE + inds[1]
                        else:
                            # user inputed raw coordinate
                            # This option is not documented in the game
                            # instructions because it is mainly for testing.
                            move = inds[0]

                        board = board.move(move)
                        quit, restart = check_game_over(board)
                        if quit:
                            return
                        elif restart:
                            board = Board()
                            human = get_team()

                        print board

                    except IndexError:
                        # move is out of bounds
                        print UTIL['index_error']

                    except LookupError:
                        # space is already occupied
                        print UTIL['lookup_error']

                    except ValueError:
                        # not an integer or improper format
                        print UTIL['input_error']
            
            except KeyboardInterrupt:
                # catch ctrl-c from user
                print UTIL['keyboard_interrupt']

            except EOFError:
                # catch ctrl-d from user and exit gracefully
                # undocumented because it provides no exit confirmation
                return


if __name__ == '__main__':
    main()
