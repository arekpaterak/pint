from ply.lex import lex
from ply.yacc import yacc

# --- Tokenizer ---

# All tokens must be named in advance.
tokens = (
          'TYPE', 'INT', 'FLOAT', 'BOOLEAN', 'STRING', 'NONE',
          'IDENTIFIER', 'CLASS', 'INHERITS', 
          'LBRACE', 'RBRACE', 'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET', 'LEFTARROW', 'RIGHTARROW',
          'COLON', 'COMMA', 'DOT', 'ASSIGN', 
          'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MODULO',
          'LESS', 'LESSEQUAL', 'GREATER', 'GREATEREQUAL', 'EQUAL', 'NOTEQUAL', 
          'AND', 'OR', 'NOT',
          'COMMENT',  
          'LIST', 'TUPLE', 'DICT', 'SET', 
          'FUNCTION', 'RETURNARROW', 'CONSTRUCTOR',
          'TREE', 'LEAF', 'FALLENLEAF',
          'LOOP',
          'BREAK', 'CONTINUE', 'RETURN', 'PASS',
          'NEWLINE',
          'SELF'
        )

# Ignored characters
t_ignore = ' \t'

# Token matching rules are written as regexs
t_TYPE = r'🔢|⏺️|🆒|🔠'

t_BOOLEAN = r'✅|❌'
t_STRING = r'\".*\"|✏️\“.*\”'
t_NONE = r'🌌'

t_IDENTIFIER = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_CLASS = r'🏛️'
t_INHERITS = r'👨‍👦'

t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LEFTARROW = r'<'
t_RIGHTARROW = r'>'

t_COLON = r':'
t_COMMA = r','
t_DOT = r'\.'
t_ASSIGN = r'='

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MODULO = r'%'

t_LESS = r'🐜'
t_LESSEQUAL = r'🐜⚖️'
t_GREATER = r'🐘'
t_GREATEREQUAL = r'🐘⚖️'
t_EQUAL = r'⚖️'

t_AND = r'and'
t_OR = r'or'
t_NOT = r'not'

# t_COMMENT = r'(💬⬇️(.|\n)*?💬⬆️\n)|(💬.*\n)'

t_LIST = r'🐍'
t_TUPLE = r'🌼'
t_DICT = r'🗺️'
t_SET = r'🗑️'

t_FUNCTION = r'🍺'
t_CONSTRUCTOR = r'🏗️'
t_RETURNARROW = r'->'

t_TREE = r'🌲'
t_LEAF = r'🍃'
t_FALLENLEAF = r'🍂'

t_LOOP = r'🔁'

t_BREAK = r'🛑'
t_CONTINUE = r'🚦'
t_RETURN = r'🦞'
t_PASS = r'🦥'

t_SELF = r'🤗'

# t_NEWLINE = r'\n'

# A function can be used if there is an associated action.
# Write the matching regex in the docstring.
def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_NEWLINE(t):
    r'\n'
    t.lexer.lineno += 1
    return t

def t_COMMENT(t):
    r'(💬⬇️(.|\n)*?💬⬆️\n)|(💬.*\n)'
    t.lexer.lineno += t.value.count('\n')
    return t

# Error handler for illegal characters
def t_error(t):
    last_cr = t.lexer.lexdata.rfind('\n', 0, t.lexpos)
    if last_cr < 0:
        last_cr = 0
    column = (t.lexpos - last_cr) + 1
    raise Exception(f'Illegal character {t.value[0]!r} at line {t.lexer.lineno}, column {column}.')
    t.lexer.skip(1)

# Build the lexer object
lexer = lex()

# --- Parser ---

start = 'program'
spacing = 4*' '

variables = {}
types = {
        '🔢': 'int',
        '🐍': 'list',
        '🌼': 'tuple',
        '🗺️': 'dict',
        '🗑️': 'set',
        '⏺️': 'float',
        '🆒': 'bool',
        '🔠': 'str'
    }

# @TODO: Add support for other emoji_operators
emoji_operators = {
        '🐜': '<',
    }

class Variable:
    def __init__(self, name, value, type):
        self.name = name
        self.value = value
        self.type = type

def indent_statements(statements):
    statements = statements.split('\n')
    statements = [spacing + statement for statement in statements]
    statements = '\n'.join(statements)
    return statements

def p_program(p):
    '''
    program : program definition
            | program statement 
            | definition
            | statement
            | empty
    '''
    p[0] = ''.join(p[1:])

def p_empty(p):
    '''
    empty :
    '''
    p[0] = ''

def p_type(p):
    '''
    type : TYPE
         | IDENTIFIER
         | LIST LEFTARROW type RIGHTARROW
         | TUPLE LEFTARROW types RIGHTARROW
         | DICT LEFTARROW type COMMA type RIGHTARROW
         | SET LEFTARROW type RIGHTARROW
    '''
    p[0] = ''.join(p[1:])

def p_types(p):
    '''
    types : types COMMA type
          | type
    '''
    pass

def p_definition(p):
    '''
    definition : class_definition
               | function_definition
    '''
    p[0] = p[1]

def p_variable_definition(p):
    '''
    variable_definition : type IDENTIFIER ASSIGN expression NEWLINE
    '''

    if p[2] in variables.keys():
        raise Exception(f'Variable {p[2]} already defined')
    
    # @TODO: Add support for type checking

    variables[p[2]] = Variable(p[2], p[4], p[1])

    # p[0] = p[2] + ': ' + types[p[1]] + ' = ' + str(p[4]) + '\n'
    p[0] = f'{p[2]}: {types[p[1]]} = {str(p[4])}\n'

def p_function_definition(p):
    '''
    function_definition : FUNCTION IDENTIFIER LPAREN parameters RPAREN RETURNARROW type LBRACE NEWLINE statements RBRACE NEWLINE
                        | FUNCTION IDENTIFIER LPAREN parameters RPAREN RETURNARROW NONE LBRACE NEWLINE statements RBRACE NEWLINE
    '''
    p[0] = f'def {p[2]}({p[4]}) -> {types[p[7]]}:\n{indent_statements(p[10])}'

# @TODO: Add support for try and raise statements
def p_statement(p):
    '''
    statement : assignment_statement 
              | call_statement
              | if_statement
              | match_statement
              | loop_statement
              | continue_statement
              | break_statement
              | variable_definition
              | return_statement
              | pass_statement
              | comment
              | NEWLINE
    '''
    p[0] = p[1]

def p_return_statement(p):
    '''
    return_statement : RETURN expression NEWLINE
                     | RETURN NEWLINE
    '''
    p[0] = 'return ' + p[2] + '\n' if len(p) > 3 else 'return\n'

def p_statements(p):
    '''
    statements : statements statement
               | statement
               | empty
    '''
    p[0] = ''.join(p[1:])

def p_assignment_statement(p):
    '''
    assignment_statement : compound_identifier ASSIGN expression NEWLINE
                         | subscript_expression ASSIGN expression NEWLINE
    '''
    # if p[1] not in variables.keys():
    #     raise Exception(f'Variable {p[1]} not defined')

    # @TODO: Add support for type checking
    # if not isinstance(p[3], variables[p[1]].type):
    #     raise Exception(f'Variable {p[1]} type mismatch')

    # variables[p[1]].value = p[3]
    p[0] = p[1] + ' = ' + p[3] + '\n'

def p_call_statement(p):
    '''
    call_statement : call NEWLINE
    '''
    pass

def p_if_statement(p):
    '''
    if_statement : simple_if_statement
                 | compound_if_statement
    '''
    pass

def p_simple_if_statement(p):
    '''
    simple_if_statement : LEAF LPAREN expression RPAREN LBRACE NEWLINE statements RBRACE NEWLINE
    '''
    pass

def p_compound_if_statement(p):
    '''
    compound_if_statement : TREE LBRACE simple_if_statements else_block RBRACE NEWLINE
                          | TREE LBRACE simple_if_statements RBRACE NEWLINE
    '''
    pass

def p_simple_if_statements(p):
    '''
    simple_if_statements : simple_if_statements simple_if_statement
                         | simple_if_statement
    '''
    pass

def p_else_block(p):
    '''
    else_block : FALLENLEAF LBRACE statements RBRACE
    '''
    pass

def p_match_statement(p):
    '''
    match_statement : TREE LPAREN compound_identifier RPAREN LBRACE NEWLINE match_cases match_default RBRACE NEWLINE
    '''
    pass

def p_match_cases(p):
    '''
    match_cases : match_cases match_case
                | match_case
    '''
    pass

def p_match_case(p):
    '''
    match_case : LEAF LPAREN expression RPAREN LBRACE statements RBRACE NEWLINE
    '''
    pass

def p_match_default(p):
    '''
    match_default : FALLENLEAF LBRACE statements RBRACE NEWLINE
    '''
    pass 

def p_loop_statement(p):
    '''
    loop_statement : while_statement
                   | for_statement
    '''
    p[0] = p[1]

# @TODO: Add other loops
def p_while_statement(p):
    '''
    while_statement : LOOP LPAREN expression RPAREN LBRACE NEWLINE statements RBRACE NEWLINE
                    | LOOP LBRACE NEWLINE statements RBRACE NEWLINE
    '''
    statements = p[7] if len(p) == 10 else p[4]
    statements = indent_statements(statements)

    p[0] = 'while ' + p[3] + ':\n' + statements if len(p) == 10 else 'while True:\n' + statements

def p_for_statement(p):
    '''
    for_statement : LOOP LPAREN type IDENTIFIER ASSIGN expression RPAREN LBRACE NEWLINE statements RBRACE NEWLINE
    '''
    pass

def p_continue_statement(p):
    '''
    continue_statement : CONTINUE NEWLINE
    '''
    pass

def p_break_statement(p):
    '''
    break_statement : BREAK NEWLINE
    '''
    pass

def p_pass_statement(p):
    '''
    pass_statement : PASS NEWLINE
    '''
    pass

def p_comment(p):
    '''
    comment : COMMENT
    '''
    comment = p[1].splitlines()
    if len(comment) > 1:
        comment[0] = comment[0].replace('💬⬇️', '\'\'\'')
        comment[-1] = comment[-1].replace('💬⬆️', '\'\'\'')
        comment = '\n'.join([line for line in comment])
    else:
        comment = comment[0].replace('💬', '#')

    p[0] = comment + '\n'

def p_parameters(p):
    '''
    parameters : parameters COMMA parameter
               | parameter
               | empty
    '''
    p[0] = p[1] + ',' + p[3] if len(p) > 2 else p[1]

def p_parameter(p):
    '''
    parameter : simple_parameter
              | default_parameter
    '''
    p[0] = p[1]

def p_simple_parameter(p):
    '''
    simple_parameter : type IDENTIFIER
    '''
    p[0] = p[2] + ':' + p[1]

def p_default_parameter(p):
    '''
    default_parameter : type IDENTIFIER ASSIGN expression
    '''
    p[0] = p[2] + ':' + p[1] + '=' + p[4]

def p_class_definition(p):
    '''
    class_definition : CLASS IDENTIFIER LBRACE NEWLINE class_body RBRACE NEWLINE
                     | CLASS IDENTIFIER INHERITS IDENTIFIER LBRACE NEWLINE class_body RBRACE NEWLINE
    '''
    if not p[2] in types.keys():
        types.update({p[2]: p[2]})
    else:
        raise Exception(f'Class {p[2]} already defined')
    
    pass

def p_class_body(p):
    '''
    class_body : fields_declarations constructor_definition methods_definitions
    '''
    pass

def p_fields_declarations(p):
    '''
    fields_declarations : fields_declarations field_declaration
                        | field_declaration
                        | empty
    '''
    pass

def p_field_declaration(p):
    '''
    field_declaration : type IDENTIFIER NEWLINE
                      | CLASS type IDENTIFIER NEWLINE
                      | NEWLINE
    '''
    pass


def p_constructor_definition(p):
    '''
    constructor_definition : CONSTRUCTOR IDENTIFIER LPAREN parameters RPAREN LBRACE NEWLINE statements RBRACE NEWLINE
                           | empty
    '''
    pass

def p_methods_definitions(p):
    '''
    methods_definitions : methods_definitions method_definition
                        | method_definition
                        | empty
    '''
    pass

def p_method_definition(p):
    '''
    method_definition : function_definition
                      | CLASS function_definition
                      | NEWLINE
    '''
    pass

def p_expression(p):
    '''
    expression : LPAREN expression RPAREN
               | binary_expression
               | unary_expression
               | call_expression
               | literal_expression
               | identifier_expression
               | subscript_expression
               | NONE
    '''
    p[0] = p[1] if len(p) == 2 else p[2]

def p_binary_operator(p):
    '''
    binary_operator : PLUS
                    | MINUS
                    | TIMES
                    | DIVIDE
                    | MODULO
                    | EQUAL
                    | NOTEQUAL
                    | LESS
                    | GREATER
                    | LESSEQUAL
                    | GREATEREQUAL
                    | AND
                    | OR
    '''
    p[0] = emoji_operators[p[1]] if p[1] in emoji_operators.keys() else p[1]

def p_binary_expression(p):
    '''
    binary_expression : expression binary_operator expression
    '''
    p[0] = ' '.join(map(str, p[1:]))

def p_unary_expression(p):
    '''
    unary_expression : MINUS expression
                     | NOT expression
    '''
    pass

def p_call_expression(p):
    '''
    call_expression : call
    '''
    pass

def p_call(p):
    '''
    call : compound_identifier LPAREN arguments RPAREN
         | LIST LPAREN arguments RPAREN
         | SET LPAREN arguments RPAREN
         | TUPLE LPAREN arguments RPAREN
         | DICT LPAREN items RPAREN
    '''
    pass

def p_items(p):
    '''
    items : items COMMA item
          | item
          | empty
    '''
    pass

def p_item(p):
    '''
    item : expression COLON expression
    '''
    pass

def p_compound_identifier(p):
    '''
    compound_identifier : compound_identifier DOT IDENTIFIER
                        | IDENTIFIER
                        | SELF DOT IDENTIFIER
    '''
    p[0] = ''.join(p[1:])

def p_arguments(p):
    '''
    arguments : arguments COMMA expression
              | expression
              | empty
    '''
    pass

def p_literal_expression(p):
    '''
    literal_expression : literal
    '''
    p[0] = p[1]

def p_literal(p):
    '''
    literal : INT
            | FLOAT
            | STRING
            | BOOLEAN
    '''
    p[0] = p[1]

def p_identifier_expression(p):
    '''
    identifier_expression : compound_identifier
    '''
    p[0] = p[1]

def p_subscript_expression(p):
    '''
    subscript_expression : expression LBRACKET expression RBRACKET
    '''
    pass

def p_error(p):
    raise Exception(f'Syntax error at {p.value!r}, line {p.lineno}, you idiot.')


with open('examples\\simple.pint', 'r', encoding="utf8") as f:
    data = f.read()

# uncomment to see the tokens (error messages in parsing don't work properly then)
# lexer.input(data)

# while True:
#     tok = lexer.token()
#     if not tok:
#         break
#     print(tok)

# build the parser
parser = yacc()

# add debug=True to see the rules being applied
result = parser.parse(data, lexer=lexer)

# uncomment to see translated code
# print(result)
