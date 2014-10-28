'''
Messages printed throughout simulation.
'''

STATIC = {
    'help': '\t"man": review rules\n' + \
        '\t"undo": undo your last move\n' + \
        '\t"reset": restart the match\n' + \
        '\t"docs": view credits and documentation\n' + \
        '\t"exit": quit application',

    'man': 'Tic Tac Toe\n' + \
        '\tPlay your piece by typing [row, col] (i.e. 1,2)\n' + \
        '\tType "help" to list additional commands.',

    'docs': 'Visit http://github.com/hkgumbs/tictactoe for more information.',
}

UTIL = {
    'index_error': 'Index value out of bounds!',
    'input_error': 'Invalid command! Type "man" to review rules.',
    'keyboard_interrupt' : 'Type "exit" to exit!',
    'lookup_error': 'This space is already occupied!',
    'undo_error': 'There are not enough moves to undo!',
}
