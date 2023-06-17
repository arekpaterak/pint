from typing import Any


class Program:
    spacing = 4*' '

    emoji_operators = {
            '🐜': '<',
            '🐜⚖️': '<=',
            '🐘': '>',
            '🐘⚖️': '>=',
            '⚖️': '=='
        }

    def __init__(self, types: dict[str, str] = {}):
        self.types = types
        self.classes = {}

    def get_type(self, type_):
        if len(type_) == 1:
            return self.types[type_]
        else:
            args = [self.get_type(t) for t in type_[1:] if t not in ('<', '>', ' ', ',')]
            return f'{self.types[type_[0]]}[{", ".join(args)}]'
        
    @classmethod
    def indent(cls, lines):
        lines = lines.split('\n')
        lines = [cls.spacing + line for line in lines]
        lines = '\n'.join(lines)
        return lines


class Scope:
    def __init__(self, name: str, parent: 'Scope' = None):
        self.name: str = name if parent is None else f'{parent.name}.{name}'
        self.parent: 'Scope' = parent
        self.variables: dict[str, Variable] = {}
        self.functions: dict[str, Function] = {}

        # uncomment to see scope - tree
        # self.level: int = 1 if parent is None else parent.level + 1
        # print("├" + self.level * 2 * "─" + " " + self.name)


    def contains_variable(self, name: str):
        if name in self.variables:
            return True
        elif self.parent is not None:
            return self.parent.contains_variable(name)
        else:
            return False

    def contains_function(self, name: str):
        if name in self.functions:
            return True
        elif self.parent is not None:
            return self.parent.contains_function(name)
        else:
            return False


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
        self.parent = None
    