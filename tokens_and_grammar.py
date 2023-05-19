from ply.lex import lex
from ply.yacc import yacc
from utils.errors import PintException
from utils.utils import *

# --- Tokenizer ---

# All tokens must be named in advance.
tokens = (
    "TYPE", "INT", "FLOAT", "BOOLEAN", "STRING", "NONE",
    "IDENTIFIER", "CLASS", "INHERITS",
    "LBRACE", "RBRACE", "LPAREN", "RPAREN", "LBRACKET", "RBRACKET", "LEFTARROW", "RIGHTARROW",
    "COLON", "COMMA", "DOT",
    "ASSIGN", "PLUSASSIGN", "MINUSASSIGN", "TIMESASSIGN", "DIVIDEASSIGN", "MODULOASSIGN", "POWERASSIGN", "FLOORASSIGN",
    "PLUS", "MINUS", "TIMES", "DIVIDE", "MODULO", "POWER", "FLOOR",
    "LESS", "LESSEQUAL", "GREATER", "GREATEREQUAL", "EQUAL", "NOTEQUAL",
    "AND", "OR", "NOT",
    "ONELINECOMMENT", "MULTILINECOMMENT",
    "LIST", "TUPLE", "DICT", "SET",
    "FUNCTION", "RETURNARROW", "CONSTRUCTOR",
    "TREE", "LEAF", "FALLENLEAF",
    "LOOP",
    "BREAK", "CONTINUE", "RETURN", "PASS",
    "NEWLINE",
    "SELF",
    "IMPORT", "FROM", "AS",
    "PRINT",
)

# Ignored characters
t_ignore = " \t"

# Token matching rules are written as regexs
t_TYPE = r"🔢|⏺️|🆒|🔠"
t_LEFTARROW = r"<"
t_RIGHTARROW = r">"

t_BOOLEAN = r"✅|❌"
t_STRING = r"\".*\"|✏️\“.*\”"
t_NONE = r"🌌"

t_IDENTIFIER = r"[a-zA-Z_][a-zA-Z0-9_]*"

t_CLASS = r"🏛️"
t_INHERITS = r"👨‍👦"
t_SELF = r"🤗"
t_CONSTRUCTOR = r"🏗️"

t_FUNCTION = r"🍺"
t_RETURNARROW = r"->"

t_LBRACE = r"\{"
t_RBRACE = r"\}"
t_LPAREN = r"\("
t_RPAREN = r"\)"
t_LBRACKET = r"\["
t_RBRACKET = r"\]"

t_COLON = r":"
t_COMMA = r","
t_DOT = r"\."

# assignment operators
t_ASSIGN = r"="
t_PLUSASSIGN = r"\+="
t_MINUSASSIGN = r"-="
t_TIMESASSIGN = r"\*="
t_DIVIDEASSIGN = r"/="
t_MODULOASSIGN = r"%="
t_POWERASSIGN = r"\^="
t_FLOORASSIGN = r"//="

# arithmetic operators
t_PLUS = r"\+"
t_MINUS = r"-"
t_TIMES = r"\*"
t_DIVIDE = r"/"
t_MODULO = r"%"
t_POWER = r"\^"
t_FLOOR = r"//"

# comparison operators
t_LESS = r"🐜"
t_LESSEQUAL = r"🐜⚖️"
t_GREATER = r"🐘"
t_GREATEREQUAL = r"🐘⚖️"
t_EQUAL = r"⚖️"

# logical operators
t_AND = r"and"
t_OR = r"or"
t_NOT = r"not"
# t_AND = r'☹️'
# t_OR = r'🙂'
# t_NOT = r'🙃'

# data structures
t_LIST = r"🐍"
t_TUPLE = r"🌼"
t_DICT = r"🗺️"
t_SET = r"🗑️"

# if and match
t_TREE = r"🌲"
t_LEAF = r"🍃"
t_FALLENLEAF = r"🍂"

# loops
t_LOOP = r"🔁"

# flow control
t_BREAK = r"🛑"
t_CONTINUE = r"🚦"
t_RETURN = r"🦞"
t_PASS = r"🦥"

# importing
t_IMPORT = r"🚢"
t_FROM = r"🏝️"
t_AS = r"🤿"

# aliases
t_PRINT = r"🖨️"

# A function can be used if there is an associated action.
# Write the matching regex in the docstring.
def t_FLOAT(t):
    r"(\+|-)?\d+\.\d+"
    t.value = float(t.value)
    return t


def t_INT(t):
    r"(\+|-)?\d+"
    t.value = int(t.value)
    return t


# t_NEWLINE = r'\n'
def t_NEWLINE(t):
    r"\n"
    t.lexer.lineno += 1
    return t


# t_COMMENT = r'(💬⬇️(.|\n)*?💬⬆️\n)|(💬.*\n)'
def t_MULTILINECOMMENT(t):
    r"💬⬇️(.|\n)*?💬⬆️\n"
    t.lexer.lineno += t.value.count("\n")
    return t


def t_ONELINECOMMENT(t):
    r"💬.*\n"
    t.lexer.lineno += 1
    return t


# Error handler for illegal characters
def t_error(t):
    last_cr = t.lexer.lexdata.rfind("\n", 0, t.lexpos)
    if last_cr < 0:
        last_cr = 0
    column = (t.lexpos - last_cr)
    raise PintException("Illegal character", "", t.lexer.lineno, column, t.value[0])


# Build the lexer object
lexer = lex()

# --- Parser ---

spacing = 4 * " "

variables = {}

types = {
    "🔢": "int",
    "⏺️": "float",
    "🆒": "bool",
    "🔠": "str",
    "🐍": "list",
    "🌼": "tuple",
    "🗺️": "dict",
    "🗑️": "set",
}

emoji_operators = {"🐜": "<", "🐜⚖️": "<=", "🐘": ">", "🐘⚖️": ">=", "⚖️": "=="}

current_scope = Scope("global", None)


def indent(lines):
    lines = lines.strip().split("\n")
    lines = [spacing + line for line in lines]
    lines = "\n".join(lines)
    return lines


def get_type(type_):
    if len(type_) == 1:
        return types[type_]
    else:
        args = [get_type(t) for t in type_[1:] if t not in ("<", ">", " ", ",")]
        return f'{types[type_[0]]}[{", ".join(args)}]'


# PROGRAM
start = "program"


def p_program(p):
    """
    program : nonexecutables imports nonexecutables definitions_and_statements nonexecutables
    """
    p[0] = "".join(p[1:])


# NEWLINES
def p_newlines(p):
    """
    newlines : newlines NEWLINE
             | NEWLINE
    """
    p[0] = "".join(p[1:])


# EMPTY
def p_empty(p):
    """
    empty :
    """
    p[0] = ""


# IMPORTS
def p_imports(p):
    """
    imports : imports nonexecutables import
            | import
            | empty
    """
    p[0] = "".join(p[1:])


def p_import(p):
    """
    import : IMPORT compound_identifier NEWLINE
           | IMPORT compound_identifier AS IDENTIFIER NEWLINE
           | IMPORT compound_identifier FROM compound_identifier NEWLINE
           | IMPORT compound_identifier FROM compound_identifier AS IDENTIFIER NEWLINE
    """

    match p[1:]:
        case ["🚢", _, "\n"]:
            p[0] = f"import {p[2]}\n"
        case ["🚢", _, "🤿", _, "\n"]:
            p[0] = f"import {p[2]} as {p[4]}\n"
        case ["🚢", _, "🏝️", _, "\n"]:
            p[0] = f"from {p[4]} import {p[2]}\n"
        case ["🚢", _, "🏝️", _, "🤿", _, "\n"]:
            p[0] = f"from {p[4]} import {p[2]} as {p[6]}\n"
        case _:
            p[0] = "\n"


# DEFINITIONS AND STATEMENTS
def p_definitions_and_statements(p):
    """
    definitions_and_statements : definitions_and_statements nonexecutables definition
                               | definitions_and_statements nonexecutables statement
                               | definition
                               | statement
                               | empty
    """
    p[0] = "".join(p[1:])


# TYPES
def p_type(p):
    """
    type : TYPE
         | IDENTIFIER
         | LIST LEFTARROW type RIGHTARROW
         | TUPLE LEFTARROW types RIGHTARROW
         | DICT LEFTARROW type COMMA type RIGHTARROW
         | SET LEFTARROW type RIGHTARROW
    """
    p[0] = (types[p[1]] + "".join(p[2:])).replace("<", "[").replace(">", "]")


def p_types(p):
    """
    types : types COMMA type
          | type
    """
    p[0] = p[1] if len(p) == 2 else ", ".join(p[1:])


# DEFINITION
def p_definition(p):
    """
    definition : class_definition
               | function_definition
               | variable_definition
    """
    p[0] = p[1]


# VARIABLE DEFINITION
def p_variable_definition(p):
    """
    variable_definition : type IDENTIFIER ASSIGN expression NEWLINE
                        | type IDENTIFIER ASSIGN expression oneline_comment
    """
    # @TODO: Add support for type checking

    global current_scope

    if current_scope.contains_variable(p[2]):
        raise PintException("Definition error", f"Variable \"{p[2]}\" already defined in scope {current_scope.name}", p.lexer.lineno - 1, 1, None)
    else:
        current_scope.variables[p[2]] = Variable(p[2], p[1], p[4])

    match p[-1]:
        case "\n":
            p[0] = f"{p[2]}: {p[1]} = {str(p[4])}\n"
        case _:
            p[0] = f"{p[2]}: {p[1]} = {str(p[4])} {p[5]}"
            

# FUNCTION DEFINITION
def p_function_definition(p):
    """
    function_definition : function_naming LPAREN parameters RPAREN RETURNARROW type LBRACE NEWLINE function_body RBRACE NEWLINE
                        | function_naming LPAREN parameters RPAREN RETURNARROW NONE LBRACE NEWLINE function_body RBRACE NEWLINE
    """
    global current_scope

    current_scope = current_scope.parent

    current_scope.functions[p[1].name].parameters = p[3]
    current_scope.functions[p[1].name].return_type = p[6]
    current_scope.functions[p[1].name].body = p[9]

    p[0] = f"def {p[1].name}({p[3]}) -> {p[6].replace('🌌', 'None')}:\n{indent(p[9])}\n"


def p_function_naming(p):
    """
    function_naming : FUNCTION IDENTIFIER
    """
    global current_scope

    if current_scope.contains_function(p[2]):
        raise PintException("Definition error", f"Function \"{p[2]}\" already defined in scope {current_scope.name}", p.lexer.lineno, 1, None)
    else:
        current_scope.functions[p[2]] = p[0] = Function(p[2], None, None, None)
        current_scope = Scope(p[2], current_scope)


def p_function_body(p):
    """
    function_body : function_body statement nonexecutables
                  | function_body variable_definition nonexecutables
                  | function_body function_definition nonexecutables
                  | nonexecutables
                  | empty
    """
    p[0] = "".join(p[1:])


# STATEMENTS
# @TODO: Add support for try and raise statements
def p_statement(p):
    """
    statement : assignment_statement
              | call_statement
              | if_statement
              | match_statement
              | loop_statement
              | continue_statement
              | break_statement
              | return_statement
              | pass_statement
              | NEWLINE
    """
    p[0] = p[1]


def p_statements(p):
    """
    statements : statements comments statement
               | statement
               | empty
    """
    p[0] = "".join(p[1:])


def p_return_statement(p):
    """
    return_statement : RETURN expression NEWLINE
                     | RETURN NEWLINE
    """
    p[0] = "return " + p[2] + "\n" if len(p) > 3 else "return\n"


# ASSIGNMENT
def p_assignment_statement(p):
    """
    assignment_statement : compound_identifier assign expression NEWLINE
                         | subscript_expression assign expression NEWLINE
                         | compound_identifier assign expression oneline_comment
                         | subscript_expression assign expression oneline_comment
    """
    # @TODO: Add support for type checking

    global current_scope

    variable_basename = (
        p[1].split(".")[0] if "." in p[1] and not "self" in p[1]
        else p[1].split(".")[1] if "." in p[1]  
        else p[1].split("[")[0] if "[" in p[1] 
        else p[1]
    )

    if not current_scope.contains_variable(variable_basename):
        raise PintException(
            "Assignment error", 
            f"Variable \"{variable_basename}\" not defined", 
            p.lexer.lineno - 1, 
            1, 
            None
        )
    
    # @TODO: compound identifiers in scope? value update? is keeping track of variable value necessary? 
    
    match p[-1]:
        case "\n":
            p[0] = f"{p[1]} {p[2]} {p[3]}\n"
        case _:
            p[0] = f"{p[1]} {p[2]} {p[3]} {p[4]}"


def p_assign(p):
    """
    assign : ASSIGN
           | PLUSASSIGN
           | MINUSASSIGN
           | TIMESASSIGN
           | DIVIDEASSIGN
           | MODULOASSIGN
           | POWERASSIGN
           | FLOORASSIGN
    """
    if p[1] == "^=":
        p[0] = "**="
    else:
        p[0] = p[1]


# CALL
def p_call_statement(p):
    """
    call_statement : call NEWLINE
    """
    p[0] = p[1] + "\n"


# IF
def p_if_statement(p):
    """
    if_statement : simple_if_statement
                 | compound_if_statement
    """
    p[0] = p[1]


def p_simple_if_statement(p):
    """
    simple_if_statement : LEAF LPAREN expression RPAREN LBRACE NEWLINE if_body RBRACE NEWLINE
    """
    p[0] = f"if {p[3]}:\n{indent(p[7])}\n"


def p_if_body(p):
    """
    if_body : if_body statement nonexecutables
            | if_body variable_definition nonexecutables
            | nonexecutables
            | empty
    """
    p[0] = "".join(p[1:])


def p_compound_if_statement(p):
    """
    compound_if_statement : TREE LBRACE NEWLINE if_elseif_statements else_block RBRACE NEWLINE
                          | TREE LBRACE NEWLINE if_elseif_statements RBRACE NEWLINE
    """
    p[0] = p[4] + p[5] if len(p) > 7 else p[4]


def p_if_elseif_statements(p):
    """
    if_elseif_statements : if_elseif_statements elseif_statement
                         | simple_if_statement
    """
    p[0] = "".join(p[1:])


def p_elseif_statement(p):
    """
    elseif_statement : LEAF LPAREN expression RPAREN LBRACE NEWLINE if_body RBRACE NEWLINE
    """
    p[0] = f"elif {p[3]}:\n{indent(p[7])}\n"


def p_else_block(p):
    """
    else_block : FALLENLEAF LBRACE NEWLINE if_body RBRACE NEWLINE
    """
    p[0] = f"else:\n{indent(p[4])}\n"


# MATCH
def p_match_statement(p):
    """
    match_statement : TREE LPAREN compound_identifier RPAREN LBRACE NEWLINE match_cases match_default RBRACE NEWLINE
    """
    pass


def p_match_cases(p):
    """
    match_cases : match_cases match_case
                | match_case
    """
    pass


def p_match_case(p):
    """
    match_case : LEAF LPAREN expression RPAREN LBRACE statements RBRACE NEWLINE
    """
    pass


def p_match_default(p):
    """
    match_default : FALLENLEAF LBRACE statements RBRACE NEWLINE
    """
    pass


# LOOP
def p_loop_statement(p):
    """
    loop_statement : while_statement
                   | for_statement
    """
    p[0] = p[1]


# WHILE, INFINITE LOOP
def p_while_statement(p):
    """
    while_statement : LOOP LPAREN expression RPAREN LBRACE NEWLINE statements RBRACE NEWLINE
                    | LOOP LBRACE NEWLINE statements RBRACE NEWLINE
    """
    statements = p[7] if len(p) == 10 else p[4]
    statements = indent(statements)

    condition = p[3] if len(p) == 10 else "True"

    p[0] = f"while {condition}:\n{statements}\n"


# FOR
def p_for_statement(p):
    """
    for_statement : LOOP LPAREN type IDENTIFIER ASSIGN expression RPAREN LBRACE NEWLINE statements RBRACE NEWLINE
    """
    p[0] = f"for {p[4]} in {p[6]}:\n{indent(p[10])}\n"


# CONTINUE, BREAK, PASS
def p_continue_statement(p):
    """
    continue_statement : CONTINUE NEWLINE
    """
    p[0] = "continue\n"


def p_break_statement(p):
    """
    break_statement : BREAK NEWLINE
    """
    p[0] = "break\n"


def p_pass_statement(p):
    """
    pass_statement : PASS NEWLINE
    """
    p[0] = "pass\n"


# COMMENTS
def p_comment(p):
    """
    comment : oneline_comment
            | multiline_comment
    """
    p[0] = p[1]


def p_multiline_comment(p):
    """
    multiline_comment : MULTILINECOMMENT
    """
    lines = p[1].replace("💬⬇️", "").replace("💬⬆️", "").strip().split("\n")
    lines = ["# " + line.strip() for line in lines]
    lines = "\n".join(lines) + "\n"

    p[0] = lines


def p_oneline_comment(p):
    """
    oneline_comment : ONELINECOMMENT
    """
    p[0] = p[1].replace("💬", "#")


def p_comments(p):
    """
    comments : comments comment
             | comment
    """
    p[0] = "".join(p[1:])


def p_nonexecutables(p):
    """
    nonexecutables : nonexecutables comments
                   | nonexecutables newlines
                   | empty
    """
    p[0] = "".join(p[1:])


# PARAMETERS
def p_parameters(p):
    """
    parameters : parameters COMMA parameter
               | parameter
               | empty
    """
    p[0] = p[1] + ", " + p[3] if len(p) > 2 else p[1]


def p_class_parameters(p):
    """
    class_parameters : parameters
    """
    p[0] = f"self, {p[1]}" if len(p[1]) > 1 else "self"


def p_parameter(p):
    """
    parameter : simple_parameter
              | default_parameter
    """
    p[0] = p[1]


def p_simple_parameter(p):
    """
    simple_parameter : type IDENTIFIER
    """
    global current_scope

    current_scope.variables[p[2]] = Variable(p[2], p[1])
    p[0] = f"{p[2]}: {p[1]}"


def p_default_parameter(p):
    """
    default_parameter : type IDENTIFIER ASSIGN expression
    """
    global current_scope

    current_scope.variables[p[2]] = Variable(p[2], p[1], p[4])
    p[0] = f"{p[2]}: {p[1]} = {p[4]}"


# CLASS


class Class:
    def __init__(self, name, cls_fields, fields, constructor, cls_methods, methods):
        self.name = name
        self.cls_fields = cls_fields
        self.fields = fields
        self.constructor = constructor
        self.cls_methods = cls_methods
        self.methods = methods

    def __str__(self):
        cls_fields = "\n".join(
            [f"{field.name}: {field.type}" for field in self.cls_fields]
        )

        # fields = '\n'.join([f'self.{field.name}: {field.type}' for field in self.fields])

        constructor = str(self.constructor) if self.constructor else ""

        cls_methods = "\n".join(map(str, self.cls_methods))

        methods = "\n".join(map(str, self.methods))

        return "\n".join([item for item in [cls_fields, constructor, cls_methods, methods] if item])


# def p_class_definition(p):
#     """
#     class_definition : CLASS IDENTIFIER LBRACE NEWLINE class_body RBRACE NEWLINE
#                      | CLASS IDENTIFIER INHERITS IDENTIFIER LBRACE NEWLINE class_body RBRACE NEWLINE
#     """

#     if not p[2] in types.keys():
#         types.update({p[2]: p[2]})
#     else:
#         # raise Exception(f"Class {p[2]} already defined")

#     # if len(p) == 8:
#     #     p[0] = f'class {p[2]}:\n{indent(p[5])}\n'
#     # else:
#     #     p[0] = f'class {p[2]}({p[4]}):\n{indent(p[7])}\n'

#     match p[3]:
#         case "👨‍👦":
#             cls: Class = p[7]
#             cls.name = p[2]
#             classes.append(cls)
#             p[0] = f"class {p[2]}({p[4]}):\n{indent(str(cls))}\n"

#         case _:
#             cls: Class = p[5]
#             cls.name = p[2]
#             classes.append(cls)
#             p[0] = f"class {p[2]}:\n{indent(str(cls))}\n"
    

def p_class_definition(p):
    """
    class_definition : class_naming LBRACE NEWLINE class_body RBRACE NEWLINE
                     | class_naming INHERITS IDENTIFIER LBRACE NEWLINE class_body RBRACE NEWLINE
    """
    global current_scope

    match p[2]:
        case "👨‍👦":
            cls: Class = p[6]
            cls.name = p[1][1]
            classes.append(cls)
            p[0] = f"class {p[1][1]}({p[3]}):\n{indent(str(cls))}\n"

        case _:
            cls: Class = p[4]
            cls.name = p[1][1]
            classes.append(cls)
            p[0] = f"class {p[1][1]}:\n{indent(str(cls))}\n"

    current_scope = current_scope.parent


def p_class_naming(p):
    """
    class_naming : CLASS IDENTIFIER
    """
    global current_scope

    if not p[2] in types.keys():
        types.update({p[2]: p[2]})
        current_scope = Scope(p[2], current_scope)
    else:
        raise PintException("Definition error", f"Class \"{p[2]}\" already defined", p.lexer.lineno, 1, None)

    p[0] = (p[1], p[2])


def p_class_body(p):
    """
    class_body : nonexecutables fields_declarations nonexecutables constructor_definition nonexecutables methods_definitions nonexecutables
    """

    # TODO: Create a Class here

    # p[0] = ''.join(p[1:])

    def split_list_by(l, p):
        yes, no = [], []
        for i in l:
            (yes if p(i) else no).append(i)
        return yes, no

    fields_declarations = p[2]
    fields_declarations = split_list_by(
        fields_declarations, lambda field: field.is_cls_field
    )

    constructor_definition = p[4]

    methods_definitions = p[6]
    methods_definitions = split_list_by(
        methods_definitions, lambda method: method.is_cls_method
    )

    p[0] = Class(
        None,
        fields_declarations[0],
        fields_declarations[1],
        constructor_definition,
        methods_definitions[0],
        methods_definitions[1],
    )


def p_fields_declarations(p):
    """
    fields_declarations : fields_declarations nonexecutables field_declaration
                        | field_declaration
                        | empty
    """

    # p[0] = ''.join(p[1:])

    match p[1:]:
        case [_, _, _]:
            p[0] = [*p[1], p[3]]
        case Field():
            p[0] = [p[1]]
        case _:
            p[0] = []


class Field:
    def __init__(self, name, type, is_cls_field: bool = False):
        self.name = name
        self.type = type
        self.is_cls_field = is_cls_field


classes = []


def p_field_declaration(p):
    """
    field_declaration : type IDENTIFIER NEWLINE
                      | CLASS type IDENTIFIER NEWLINE
    """
    global current_scope

    match p[1:]:
        case [_, _, _]:
            if current_scope.contains_variable(p[2]):
                raise PintException("Definition error", f"Field \"{p[2]}\" already defined in scope {current_scope.name}", p.lexer.lineno - 2, 1, None)
            else:
                current_scope.variables[p[2]] = Variable(p[2], p[1], None)
                p[0] = Field(p[2], p[1])

            # identifier = p[2]

            # if identifier in current_class.fields.keys():
            #     raise Exception(f'Field {identifier} already defined')

            # field = Variable(identifier, None, p[1])
            # current_class.fields[identifier] = field

            # p[0] = Field(identifier, p[1])

        case ["🏛️", _, _, _]:
            if current_scope.contains_variable(p[3]):
                raise PintException("Definition error", f"Field \"{p[3]}\" already defined in scope {current_scope.name}", p.lexer.lineno, 1, None)
            else:
                current_scope.variables[p[3]] = current_scope.variables[f"self.{p[3]}"] = Variable(p[3], p[2], None)
                p[0] = Field(p[3], p[2], True)
            # identifier = p[3]

            # if identifier in current_class.cls_fields.keys():
            #     raise Exception(f'Field {identifier} already defined')

            # cls_field = Variable(identifier, None, p[2])
            # current_class.cls_fields[identifier] = cls_field

            # p[0] = f'{identifier}: {p[2]}\n'

            # p[0] = Field(identifier, p[2], True)


# CONSTRUCTOR


class Constructor:
    def __init__(self, parameters, statements):
        self.parameters = parameters
        self.statements = statements

    def __str__(self):
        return f"def __init__({self.parameters}):\n{indent(self.statements)}\n" if self.parameters else f"def __init__(self):\n{indent(self.statements)}\n"


def p_constructor_definition(p):
    """
    constructor_definition : CONSTRUCTOR IDENTIFIER LPAREN class_parameters RPAREN LBRACE NEWLINE function_body RBRACE NEWLINE
                           | empty
    """
    # @TODO constructor scope
    if len(p) > 2:
        # p[0] = f"def __init__({p[4]}):\n{indent(p[8])}\n"
        p[0] = Constructor(p[4], p[8])
    else:
        p[0] = ""


# METHODS


class Function:
    def __init__(self, name, parameters, return_type, body):
        self.name = name
        self.parameters = parameters
        self.return_type = return_type
        self.body = body

    def __str__(self):
        return f"def {self.name}({self.parameters}) -> {self.return_type}:\n{indent(self.body)}\n"


class Method(Function):
    def __init__(self, name, parameters, return_type, body, is_cls_method: bool = False):
        super().__init__(name, parameters, return_type, body)
        self.is_cls_method = is_cls_method

    def __str__(self):
        return f"@classmethod\n{super().__str__()}".replace("self", "cls") if self.is_cls_method else super().__str__()


def p_methods_definitions(p):
    """
    methods_definitions : methods_definitions nonexecutables method_definition
                        | method_definition
                        | empty
    """
    # p[0] = ''.join(p[1:])

    match p[1:]:
        case [_, _, _]:
            p[0] = [*p[1], p[3]]
        case [Method()]:
            p[0] = [p[1]]
        case _:
            p[0] = []


def p_method_definition(p):
    """
    method_definition : method_naming LPAREN class_parameters RPAREN RETURNARROW type LBRACE NEWLINE function_body RBRACE NEWLINE
                      | method_naming LPAREN class_parameters RPAREN RETURNARROW NONE LBRACE NEWLINE function_body RBRACE NEWLINE
    """
    global current_scope

    is_cls_method = p[1].is_cls_method 
    name = p[1].name
    type = p[6].replace("🌌", "None")

    # match p[6]:
    #     case "🌌":
    #         m = Method(name, p[3], "None", p[9], is_cls_method)
    #         # p[0] = m

    #     case _:
    #         m = Method(name, p[3], p[6], p[9], is_cls_method)
    #         # p[0] = m

    p[0] = current_scope.functions[name] = Method(name, p[3], type, p[9], is_cls_method)
    current_scope = current_scope.parent


def p_method_naming(p):
    """
    method_naming : FUNCTION IDENTIFIER
                  | CLASS FUNCTION IDENTIFIER
    """
    global current_scope

    match p[1:]:
        case [_, _]:
            if current_scope.contains_function(p[2]):
                raise PintException("Definition error", f"Method \"{p[2]}\" already defined in scope {current_scope.name}", p.lexer.lineno, 1, None)
            else:
                m = Method(p[2], None, None, None)
                current_scope.functions[p[2]] = m
                current_scope = Scope(p[2], current_scope)
        case _:
            if current_scope.contains_function(p[3]):
                raise PintException("Definition error", f"Method \"{p[3]}\" already defined in scope {current_scope.name}", p.lexer.lineno, 1, None)
            else:
                m = Method(p[3], None, None, None, True)
                current_scope.functions[p[3]] = m
                current_scope = Scope(p[3], current_scope)

    p[0] = m


def p_expression(p):
    """
    expression : LPAREN expression RPAREN
               | binary_expression
               | unary_expression
               | call_expression
               | literal_expression
               | identifier_expression
               | subscript_expression
    """
    # TODO split into categories: expressions should be less ambiguous, e.g. if statement should accept only boolean expressions 
    p[0] = p[1] if len(p) == 2 else p[2]


def p_binary_operator(p):
    """
    binary_operator : PLUS
                    | MINUS
                    | TIMES
                    | DIVIDE
                    | MODULO
                    | POWER
                    | FLOOR
                    | EQUAL
                    | NOTEQUAL
                    | LESS
                    | GREATER
                    | LESSEQUAL
                    | GREATEREQUAL
                    | AND
                    | OR
    """
    if p[1] == "^":
        p[0] = "**"
    else:
        p[0] = emoji_operators[p[1]] if p[1] in emoji_operators.keys() else p[1]


def p_binary_expression(p):
    """
    binary_expression : expression binary_operator expression
    """
    p[0] = " ".join(map(str, p[1:]))


def p_unary_expression(p):
    """
    unary_expression : MINUS expression
                     | NOT expression
    """
    p[0] = f"{p[1]}{p[2]}"


def p_call_expression(p):
    """
    call_expression : call
    """
    p[0] = p[1]


def p_call(p):
    """
    call : compound_identifier LPAREN arguments RPAREN
         | LIST LPAREN arguments RPAREN
         | SET LPAREN arguments RPAREN
         | TUPLE LPAREN arguments RPAREN
         | DICT LPAREN items RPAREN
         | PRINT LPAREN arguments RPAREN
    """
    if p[1] in types.keys():
        # @TODO Match types
        p[0] = f"{types[p[1]]}({p[3]})"
    elif p[1] == "🖨️":
        p[0] = f"print({p[3]})"
    else:
        p[0] = f"{p[1]}({p[3]})"


def p_items(p):
    """
    items : items COMMA item
          | item
          | empty
    """
    p[0] = f"{p[1], p[3]}" if len(p) > 2 else p[1]


def p_item(p):
    """
    item : expression COLON expression
    """
    p[0] = f"{p[1]}: {p[3]}"


def p_compound_identifier(p):
    """
    compound_identifier : compound_identifier DOT IDENTIFIER
                        | IDENTIFIER
                        | SELF DOT IDENTIFIER
                        | INHERITS DOT IDENTIFIER
                        | INHERITS
    """
    match p[1:]:
        case ["🤗", _, _]:
            p[0] = f"self.{p[3]}"
        case ["👨‍👦", _, _]:
            p[0] = f"super().{p[3]}"
        case ["👨‍👦"]:
            p[0] = "super"
        case _:
            p[0] = "".join(p[1:])


# def p_self_identifier(p):
#     '''
#     self_identifier : SELF DOT IDENTIFIER
#     '''
#     p[0] = ''.join(p[1:])


def p_arguments(p):
    """
    arguments : arguments COMMA expression
              | expression
              | empty
    """
    p[0] = str(p[1]) + ", " + str(p[3]) if len(p) > 2 else str(p[1])


def p_literal_expression(p):
    """
    literal_expression : literal
    """
    p[0] = p[1]


def p_literal(p):
    """
    literal : INT
            | FLOAT
            | STRING
            | BOOLEAN
            | NONE
    """
    if str(p[1]) in "✅❌🌌":
        p[0] = p[1].replace("✅", "True").replace("❌", "False").replace("🌌", "None")
    else:
        p[0] = p[1]


def p_identifier_expression(p):
    """
    identifier_expression : compound_identifier
    """
    p[0] = p[1]


def p_subscript_expression(p):
    """
    subscript_expression : expression LBRACKET expression RBRACKET
    """
    p[0] = "".join(p[1:])


def p_error(p):
    last_cr = p.lexer.lexdata.rfind("\n", 0, p.lexpos)
    if last_cr < 0:
        last_cr = 0
    column = (p.lexpos - last_cr)

    raise PintException("Syntax error", "", p.lineno, column, p.value)


# uncomment to see the tokens (error messages in parsing don't work properly then)
# lexer.input(data) 

# while True:
#     tok = lexer.token()
#     if not tok:
#         break
#     print(tok)

# build the parser
parser = yacc()
