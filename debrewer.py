from tokens_and_grammar import lexer, parser

import sys
import os

if len(sys.argv) > 1:
    try:
        with open(sys.argv[1], 'r', encoding="utf8") as f:
            data = f.read()
    except:
        print(f'File {sys.argv[1]} not found.')
        exit()
else:
    raise Exception('No input file provided. Use: python debrewer.py <input_file> [-o <output_file>] [-t]')

if data[-1] != '\n':
    data += '\n'

# add debug=True to see the rules being applied
result = parser.parse(data, lexer=lexer)

# @TODO Add checking extensions and spliting file name
match sys.argv[1:]:
    case [_]:
        output_file = os.path.basename(sys.argv[1]).replace('.pint', '.py')
        with open(output_file, 'w', encoding="utf8") as f:
            f.write(result)
    case [_, '-o', _]:
        with open(sys.argv[3], 'w', encoding="utf8") as f:
            f.write(result)
    case [_, '-t']:
        print(result, end='')
