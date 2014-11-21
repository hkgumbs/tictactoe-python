'''Messages printed throughout simulation.'''

INFO = {
    'help': '\t"man": review rules\n' + \
            '\t"undo": undo your last move\n' + \
            '\t"print": display board\n' + \
            '\t"docs": view credits and documentation\n' + \
            '\t"quit": quit match',

    'man': 'Tic Tac Toe\n' + \
            '\tPlay piece by typing the number of the target space:\n' + \
            '\n'.join([
                    '\t  0 | 1 | 2 ',
                    '\t -----------',
                    '\t  3 | 4 | 5 ',
                    '\t -----------',
                    '\t  6 | 7 | 8 ']) + '\n' + \
            '\tType "help" to list additional commands.',

    'docs': 'Visit http://github.com/hkgumbs/tictactoe for more information.',
}

UTIL = {
        'input_error': 'Invalid input!',
        'lookup_error': 'This space is already occupied!',
        'undo_error': 'There are not enough moves to undo!',

        'keyboard_interrupt' : 'Type "exit" to exit!',

        'reset_confirm': 'Are you sure you want to start over? (y/n) ',
        'exit_confirm': 'Are you sure you quit the application? (y/n) ',

        'team_prompt': 'Do you want to go first? (y/n) ',
        'retry_prompt': 'Do you want to play again? (y/n) ',

        'tie_game': 'Tie game!',
        'lose_game': 'You lost!',
}

# valid input entries to binary prompts
YES = ['y', 'Y', 'yes', 'YES']
NO = ['n', 'N', 'no', 'NO']
BINARY = YES + NO

# valid commands for player
ACTIONS = ['undo', 'print', 'quit']
