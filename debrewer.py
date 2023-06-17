from tokens_and_grammar import lexer, parser
from utils.errors import PintException, DebrewerException, MyPyError

import sys
from sys import exit
import os

try:
    if len(sys.argv) > 1:
        input_file = sys.argv[1]

        input_pathname, input_extension = os.path.splitext(input_file)
        if input_extension not in ('.pint', '.🍺'):
            raise DebrewerException(f'File {sys.argv[1]} doesn\'t have a proper extension to be a Pint program.')

        try:
            with open(input_file, 'r', encoding="utf8") as f:
                program = f.read()
        except:
            raise DebrewerException(f'File {input_file} not found.')
    else:
        raise DebrewerException('No input file provided. Use: python debrewer.py <input_file> [-o <output_file>] [-t]')

except Exception as e:
    print(e)
    exit()

if program[-1] != '\n':
    program += '\n'

check_types = False

output_file = None
try:
    match sys.argv[1:]:
        case [_]:
            # output_file = os.path.basename(sys.argv[1]).replace('.pint', '.py')
            # output_file = os.path.basename(input_pathname) + '.py'
            output_file = input_pathname + '.py'
        case [_, '-o', _]:
            output_file = sys.argv[3]

            output_extension = os.path.splitext(output_file)[1]
            if output_extension != '.py':
                raise DebrewerException(f'Output file {output_file} doesn\'t have a proper extension to be a Python program.')
        case [_, '-t']:
            output_file = input_pathname + '.py'
            check_types = True
            pass
        case [_, '-o']:
            raise DebrewerException('No output file provided while -o used. Use: python debrewer.py <input_file> [-o <output_file>] [-t]')
        case _:
            raise DebrewerException('Invalid arguments. Use: python debrewer.py <input_file> [-o <output_file>] [-t]')

except Exception as e:
    print(e)
    exit()

try:
    # add debug=True to see the rules being applied
    # result = parser.parse(program, lexer=lexer, debug=True)
    result = parser.parse(program, lexer=lexer)
except PintException as e:
    line = program.split('\n')[e.line - 1]
    # print(f"{e}\n{PintExceeption.format_error_line(line, e.column - 1, e.symbol)}")
    PintException.display(input_file, line, e)
    exit()
except Exception as e:
    print(e)
    exit()

if output_file:
    with open(output_file, 'w', encoding="utf8") as f:
        f.write(result)
else:
    print(result, end='')

# calling mypy
if check_types:
    import subprocess

    # debug
    command = f"mypy {output_file} --strict --hide-error-codes --no-error-summary --pretty" # remove --pretty not to see .py context
    output = subprocess.run(command, capture_output=True, text=True).stdout
    print(output)
    print("\n" + "-" * 80 + "\n")

    # production
    command = f"mypy {output_file} --strict --hide-error-codes --no-error-summary"
    output = subprocess.run(command, capture_output=True, text=True).stdout

    messages = [message[message.find("error")+7:] for message in output.split("\n") if message != ""]
    errors = [MyPyError("Error", message) for message in messages]
    
    for error in errors:
        print(error)

print(f"\n{DebrewerException.green_color}Transpilation succesfull!{DebrewerException.reset_color}")
 