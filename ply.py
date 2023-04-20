from ply.lex import lex
from ply.yacc import yacc

# --- Tokenizer ---

# All tokens must be named in advance.
tokens = (
          'TYPE', 'INT', 'FLOAT', 'BOOLEAN', 'STRING', 'NONE',
          'IDENTIFIER', 'CLASS', 'INHERITS', 
          'LBRACE', 'RBRACE', 'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET',
          'SEMICOLON', 'COLON', 'COMMA', 'DOT', 'ASSIGN', 
          'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
          'LESS', 'LESSEQUAL', 'GREATER', 'GREATEREQUAL', 'EQUAL', 'NOTEQUAL', 
          'COMMENT',  
          'LIST', 'TUPLE', 'DICT', 'SET', 
          'FUNCTION', 'RETURNTYPE', 
          'TREE', 'LEAF', 'FALLENLEAF',
          'LOOP',
          'BREAK', 'CONTINUE', 'RETURN', 'PASS'
        )

# Ignored characters
t_ignore = ' \t'

# Token matching rules are written as regexs
t_TYPE = r'🔢|⏺️|🆒|🔠'

# t_INT = r'\d+'
# t_FLOAT = r'\d+\.\d+'
t_BOOLEAN = r'✅|❌'
t_STRING = r'\".*\"'
t_NONE = r'🌌'

t_IDENTIFIER = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_CLASS = r'🏛️'
t_INHERITS = r'<inherits>'

t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'

t_SEMICOLON = r';'
t_COLON = r':'
t_COMMA = r','
t_DOT = r'\.'
t_ASSIGN = r'◀️|='

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'

t_LESS = r'🐜|<'
t_LESSEQUAL = r'🐜⚖️|<='
t_GREATER = r'🐘|>'
t_GREATEREQUAL = r'🐘⚖️|>='
t_EQUAL = r'⚖️|=='

t_COMMENT = r'(💬⬇️(.|\n)*?💬⬆️)|(💬.*)'

t_LIST = r'🐍'
t_TUPLE = r'Tuple'
t_DICT = r'🗺️'
t_SET = r'🗑️'

t_FUNCTION = r'<function>'
t_RETURNTYPE = r'->'

t_TREE = r'🌲'
t_LEAF = r'🍃'
t_FALLENLEAF = r'🍂'

t_LOOP = r'🔁'

t_BREAK = r'🛑'
t_CONTINUE = r'🚦'
t_RETURN = r'🦞'
t_PASS = r'🦥'

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

# Ignored token with an action associated with it
def t_ignore_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')

# Error handler for illegal characters
def t_error(t):
    print(f'Illegal character {t.value[0]!r}')
    t.lexer.skip(1)

# Build the lexer object
lexer = lex()

# --- Parser ---

start = 'program'

variables = {}

class Variable:
    def __init__(self, name, value, type):
        self.name = name
        self.value = value
        self.type = type

def p_program(p):
    '''
    program : program definition
            | program statement 
            | definition
            | statement
            | empty
    '''
    p[0] = p[1]

def p_empty(p):
    '''
    empty :
    '''
    pass

def p_definition(p):
    '''
    definition : class_definition
               | function_definition
               | variable_definition
    '''
    p[0] = p[1]

def p_variable_definition(p):
    '''
    variable_definition : type IDENTIFIER ASSIGN expression NEWLINE
    '''
    if p[2] in variables.keys():
        raise Exception(f'Variable {p[2]} already defined')
    
    if not isinstance(p[4], p[1]):
        raise Exception(f'Variable {p[2]} type mismatch')

    variables[p[2]] = Variable(p[2], p[4], p[1])

def p_error(p):
    raise Exception(f'Syntax error at {p.value!r}')

# examples

# def p_expression(p):
#     '''
#     expression : term PLUS term
#                | term MINUS term
#     '''
#     # p is a sequence that represents rule contents.
#     #
#     # expression : term PLUS term
#     #   p[0]     : p[1] p[2] p[3]
#     # 
#     p[0] = ('binop', p[2], p[1], p[3])

# def p_expression_term(p):
#     '''
#     expression : term
#     '''
#     p[0] = p[1]

# def p_term(p):
#     '''
#     term : factor TIMES factor
#          | factor DIVIDE factor
#     '''
#     p[0] = ('binop', p[2], p[1], p[3])

# def p_term_factor(p):
#     '''
#     term : factor
#     '''
#     p[0] = p[1]

# def p_factor_number(p):
#     '''
#     factor : NUMBER
#     '''
#     p[0] = ('number', p[1])

# def p_factor_name(p):
#     '''
#     factor : NAME
#     '''
#     p[0] = ('name', p[1])

# def p_factor_unary(p):
#     '''
#     factor : PLUS factor
#            | MINUS factor
#     '''
#     p[0] = ('unary', p[1], p[2])

# def p_factor_grouped(p):
#     '''
#     factor : LPAREN expression RPAREN
#     '''
#     p[0] = ('grouped', p[2])

# def p_error(p):
#     print(f'Syntax error at {p.value!r}')


with open('examples\\quicksort.pint', 'r', encoding="utf8") as f:
    data = f.read()

lexer.input(data)

while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)


# Build the parser
parser = yacc()