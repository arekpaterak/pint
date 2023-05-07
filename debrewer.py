from tokens_and_grammar import lexer, parser

import sys

if len(sys.argv) > 1:
    try:
        with open(sys.argv[1], 'r', encoding="utf8") as f:
            data = f.read()
    except:
        print(f'File {sys.argv[1]} not found.')
        exit()
else:
    # raise Exception('No input file provided.')
    with open('examples\\simple.pint', 'r', encoding="utf8") as f:
        data =  f.read()

if data[-1] != '\n':
    data += '\n'

# add debug=True to see the rules being applied
result = parser.parse(data, lexer=lexer)

# @TODO Add checking extensions and spliting file name
match sys.argv[1:]:
    case [_]:
        with open(f'{sys.argv[1].split(".")[0]}.py', 'w', encoding="utf8") as f:
            f.write(result)
    case [_, '-o', _]:
        with open(sys.argv[3], 'w', encoding="utf8") as f:
            f.write(result)
    case [_, '-t']:
        print(result, end='')
