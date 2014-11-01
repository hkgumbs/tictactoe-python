'''
Messages printed throughout simulation.
'''

STATIC = {
    'help': '\t"man": review rules\n' + \
        '\t"undo": undo your last move\n' + \
        '\t"print": display board\n' + \
        '\t"reset": start match over\n' + \
        '\t"docs": view credits and documentation\n' + \
        '\t"exit": quit application',

    'man': 'Tic Tac Toe\n' + \
        '\tPlay your piece by typing [x, y] coordinate (i.e. 1,2)\n' + \
        '\tType "help" to list additional commands.',

    'docs': 'Visit http://github.com/hkgumbs/tictactoe for more information.',
}

UTIL = {
    'index_error': 'Index value out of bounds!',
    'input_error': 'Invalid command! Type "man" to review rules.',
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

# valid input entries to confirm prompts
CONFIRM = ('y', 'Y', 'yes', 'YES')
