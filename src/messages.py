'''Messages printed throughout simulation.'''

STATIC = {
    'help': '\t"man": review rules\n' + \
        '\t"undo": undo your last move\n' + \
        '\t"print": display board\n' + \
        '\t"docs": view credits and documentation\n' + \
        '\t"quit": quit match',

    'man': 'Tic Tac Toe\n' + \
        '\tPlay your piece by typing the integer order of the space (0-8)\n' + \
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
