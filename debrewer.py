from tokens_and_grammar import lexer, parser

import sys
import os


if len(sys.argv) > 1:
    input_file = sys.argv[1]

    input_pathname, input_extension = os.path.splitext(input_file)
    if input_extension not in ('.pint', '.🍺'):
        raise Exception(f'File {sys.argv[1]} doesn\'t have a proper extension to be a Pint program.')

    try:
        with open(input_file, 'r', encoding="utf8") as f:
            program = f.read()
    except:
        print(f'File {input_file} not found.')
        exit()
else:
    raise Exception('No input file provided. Use: python debrewer.py <input_file> [-o <output_file>] [-t]')

if program[-1] != '\n':
    program += '\n'

output_file = None
match sys.argv[1:]:
    case [_]:
        # output_file = os.path.basename(sys.argv[1]).replace('.pint', '.py')
        # output_file = os.path.basename(input_pathname) + '.py'
        output_file = input_pathname + '.py'
    case [_, '-o', _]:
        output_file = sys.argv[3]

        output_extension = os.path.splitext(output_file)[1]
        if output_extension != '.py':
            raise Exception(f'Output file {output_file} doesn\'t have a proper extension to be a Python program.')
    case [_, '-t']:
        pass
    case [_, '-o']:
        raise Exception('No output file provided while -o used. Use: python debrewer.py <input_file> [-o <output_file>] [-t]')
    case _:
        raise Exception('Invalid arguments. Use: python debrewer.py <input_file> [-o <output_file>] [-t]')

# add debug=True to see the rules being applied
# result = parser.parse(program, lexer=lexer, debug=True)
result = parser.parse(program, lexer=lexer)

if output_file:
    with open(output_file, 'w', encoding="utf8") as f:
        f.write(result)
else:
    print(result, end='')
