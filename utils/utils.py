from typing import Any

spacing = 4*' '

emoji_operators = {
        '🐜': '<',
        '🐜⚖️': '<=',
        '🐘': '>',
        '🐘⚖️': '>=',
        '⚖️': '=='
    }


def indent(lines):
    lines = lines.split('\n')
    lines = [spacing + line for line in lines]
    lines = '\n'.join(lines)
    return lines


class Program:
    def __init__(self, types: dict[str, str] = {}):
        self.types = types
        self.classes = {}

    def get_type(self, type_):
        if len(type_) == 1:
            return self.types[type_]
        else:
            args = [self.get_type(t) for t in type_[1:] if t not in ('<', '>', ' ', ',')]
            return f'{self.types[type_[0]]}[{", ".join(args)}]'


class Scope:
    def __init__(self, parent: 'Scope' = None):
        self.parent: 'Scope' = parent
        self.variables: dict[str, Variable] = {}
        self.functions: dict[str, Function] = {}


class Variable:
    def __init__(self, name: str, type: str, value: Any = None):
        self.name: str = name
        self.type: str = type
        self.value: Any = value


class Function:
    def __init__(self, name: str, parameters: dict[str, Variable], return_type: str, body):
        self.name = name
        self.parameters: dict = parameters
        self.return_type = return_type
        self.body = body


class Class:
    def __init__(self, name: str):
        self.name: str = name
        self.cls_fields = {}
        self.fields: dict[str, Variable] = {}
        self.constructor = None
        self.methods: dict[str, Function] = {}
        self.cls_methods = []
    