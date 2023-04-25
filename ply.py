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
          'AND', 'OR', 'NOT',
          'COMMENT',  
          'LIST', 'TUPLE', 'DICT', 'SET', 
          'FUNCTION', 'RETURNTYPE', 'CONSTRUCTOR',
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
t_STRING = r'\".*\"|✏️\“({}|.)*\”'
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

t_AND = r'and'
t_OR = r'or'
t_NOT = r'not'

t_COMMENT = r'(💬⬇️(.|\n)*?💬⬆️)|(💬.*)'

t_LIST = r'🐍'
t_TUPLE = r'Tuple'
t_DICT = r'🗺️'
t_SET = r'🗑️'

t_FUNCTION = r'<function>'
t_CONSTRUCTOR = r'<constructor>'
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
            | program comment
            | definition
            | statement
            | comment
            | empty
    '''
    p[0] = p[1]

def p_empty(p):
    '''
    empty :
    '''
    pass

def p_comment(p):
    '''
    comment : COMMENT
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
    variable_definition : TYPE IDENTIFIER ASSIGN expression SEMICOLON
    '''
    types = {
        "🔢": int,
        "⏺️": float,
        "🆒": bool,
        "🔠": str
    }

    if p[2] in variables.keys():
        raise Exception(f'Variable {p[2]} already defined')
    
    # @TODO: Add support for type checking

    variables[p[2]] = Variable(p[2], p[4], p[1])

def p_function_definition(p):
    '''
    function_definition : FUNCTION IDENTIFIER LPAREN parameters RPAREN RETURNTYPE TYPE LBRACE statements RBRACE
    '''
    pass

# @TODO: Add support for try and raise statements
def p_statement(p):
    '''
    statement : assignment_statement
              | call_statement
              | if_statement
              | loop_statement
              | continue_statement
              | break_statement
              | variable_definition
    '''
    p[0] = p[1]

def p_statements(p):
    '''
    statements : statements statement
               | statement
               | empty
    '''
    pass

def p_assignment_statement(p):
    '''
    assignment_statement : IDENTIFIER ASSIGN expression SEMICOLON
    '''
    if p[1] not in variables.keys():
        raise Exception(f'Variable {p[1]} not defined')

    # @TODO: Add support for type checking
    # if not isinstance(p[3], variables[p[1]].type):
    #     raise Exception(f'Variable {p[1]} type mismatch')

    variables[p[1]].value = p[3]

def p_call_statement(p):
    '''
    call_statement : call SEMICOLON
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
    simple_if_statement : LEAF expression LBRACE statements RBRACE
    '''
    pass

def p_simple_if_statements(p):
    '''
    simple_if_statements : simple_if_statements simple_if_statement
                         | simple_if_statement
    '''
    pass

def p_compound_if_statement(p):
    '''
    compound_if_statement : TREE LBRACE simple_if_statements else_statement RBRACE
    '''
    pass

def p_else_statement(p):
    '''
    else_statement : FALLENLEAF LBRACE statements RBRACE
                   | empty
    '''
    pass

# @TODO: Add other loops
def p_loop_statement(p):
    '''
    loop_statement : LOOP LPAREN expression RPAREN LBRACE statements RBRACE
    '''
    pass

def p_continue_statement(p):
    '''
    continue_statement : CONTINUE SEMICOLON
    '''
    pass

def p_break_statement(p):
    '''
    break_statement : BREAK SEMICOLON
    '''
    pass

def p_parameters(p):
    '''
    parameters : parameters COMMA parameter
               | parameter
               | empty
    '''
    pass

def p_parameter(p):
    '''
    parameter : TYPE IDENTIFIER 
              | TYPE IDENTIFIER ASSIGN expression
    '''
    pass

def p_class_definition(p):
    '''
    class_definition : CLASS IDENTIFIER LBRACE class_body RBRACE
                     | CLASS IDENTIFIER INHERITS IDENTIFIER LBRACE class_body RBRACE
    '''
    pass

def p_class_body(p):
    '''
    class_body : field_declarations constructor_definition method_definitions
    '''
    pass

def p_field_declaration(p):
    '''
    field_declaration : TYPE IDENTIFIER SEMICOLON
    '''
    pass

def p_field_declarations(p):
    '''
    field_declarations : field_declarations field_declaration
                       | field_declaration
                       | empty
    '''
    pass

def p_constructor_definition(p):
    '''
    constructor_definition : CONSTRUCTOR IDENTIFIER LPAREN parameters RPAREN LBRACE statements RBRACE
                           | empty
    '''
    pass

def p_method_definition(p):
    '''
    method_definition : function_definition
    '''
    pass

def p_method_definitions(p):
    '''
    method_definitions : method_definitions method_definition
                       | method_definition
                       | empty
    '''
    pass

def p_expression(p):
    '''
    expression : LPAREN expression RPAREN
               | binary_expression
               | unary_expression
               | call_expression
               | literal_expression
               | IDENTIFIER_expression
    '''
    pass

def p_binary_expression(p):
    '''
    binary_expression : expression PLUS expression
                      | expression MINUS expression
                      | expression TIMES expression
                      | expression DIVIDE expression
                      | expression EQUAL expression
                      | expression NOTEQUAL expression
                      | expression LESS expression
                      | expression GREATER expression
                      | expression LESSEQUAL expression
                      | expression GREATEREQUAL expression
                      | expression AND expression
                      | expression OR expression
    '''
    pass

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
    '''
    pass

def p_compound_identifier(p):
    '''
    compound_identifier : IDENTIFIER
                        | compound_identifier DOT IDENTIFIER
    '''
    pass

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
    pass

def p_literal(p):
    '''
    literal : INT
            | FLOAT
            | STRING
            | BOOLEAN
    '''
    pass

def p_IDENTIFIER_expression(p):
    '''
    IDENTIFIER_expression : IDENTIFIER
    '''
    pass

def p_error(p):
    raise Exception(f'Syntax error at {p.value!r}. Our fault XD sowwy.')



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


with open('examples\\simple.pint', 'r', encoding="utf8") as f:
    data = f.read()

lexer.input(data)

while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)


# Build the parser
parser = yacc()

result = parser.parse(data, lexer=lexer)
print(result)