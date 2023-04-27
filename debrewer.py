from tokens_and_grammar import lexer, parser

import sys

if (len(sys.argv) > 1):
    try:
        with open(sys.argv[1], 'r', encoding="utf8") as f:
            data = f.read()
    except:
        print(f'File {sys.argv[1]} not found.')
        exit()
else:
    with open('examples\\simple.pint', 'r', encoding="utf8") as f:
        data =  f.read()

if data[-1] != '\n':
    data += '\n'

# add debug=True to see the rules being applied
result = parser.parse(data, lexer=lexer)

# uncomment to see translated code
print(result, end='')
