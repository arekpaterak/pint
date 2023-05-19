class DebrewerException(Exception):
    yellow_color = '\033[93m'
    reset_color = '\033[0m'

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f"{self.yellow_color}Debrewer error{self.reset_color}:\n{self.message}"
    

# class PintException(Exception):
#     red_color = '\033[91m'
#     reset_color = '\033[0m'

#     def __init__(self, message, line, column, symbol):
#         self.message = message
#         self.line = line
#         self.column = column
#         self.symbol = symbol 

#     def __str__(self):
#         return f"{self.red_color}{self.message}{self.reset_color}: {self.symbol if not self.symbol.isspace() else ''} at line {self.line}, column {self.column}, you 🤡!"

#     @classmethod
#     def format_error_line(cls, code_line, start, symbol):
#         end = start + len(symbol)

#         formatted_message = code_line[:start] + cls.red_color + code_line[start:end] + cls.reset_color + code_line[end:]
#         formatted_message += '\n' + ' ' * start + cls.red_color + '^' * len(symbol) + cls.reset_color
        
#         return formatted_message
    
class PintException(Exception):
    red_color = '\033[91m'
    reset_color = '\033[0m'
    congratulations = "Congratulations, you 🤡!"

    def __init__(self, category, message, line, column, symbol):
        self.category = category
        self.message = message
        self.line = line
        self.column = column
        self.symbol = symbol 

    def __str__(self):
        return f"{self.red_color}{self.category}{self.reset_color}: {self.message}"

    def format_code_line(self, code_line):
        start = self.column - 1
        if self.symbol is None:
            end = len(code_line)
        else:
            end = start + len(self.symbol)

        padding = (len(str(self.line))+1)*" "
        sep = " | "

        output = []
        output.append(padding + sep)
        output.append(" " + str(self.line) + sep + code_line[:start] + self.red_color + code_line[start:end] + self.reset_color + code_line[end:])
        output.append(padding + sep + " " * start + self.red_color + '^' * (end - start) + self.reset_color)
        
        return "\n".join(output)
    
    @classmethod
    def display(cls, filename, code_line, e):
        output = [f"{e}"]

        output.append(f"In {filename} [{e.line}:{e.column}]:")

        output.append(e.format_code_line(code_line))

        output.append(cls.congratulations)

        print("\n".join(output))


# class DefinitionError(Exception):
#     red_color = '\033[91m'
#     reset_color = '\033[0m'
#     congratulations = "Congratulations, you 🤡!"

#     def __init__(self, type, message, line, column, content):
#         self.type = type
#         self.message = message
#         self.line = line
#         self.column = column
#         self.content = content

#     def __str__(self):
#         return f"{self.red_color}{self.type}{self.reset_color}: {self.message}"
    
#     def format_code(self, program):
#         program_lines = program.split('\n')

#         content_lines = self.content.split('\n')

#         start = self.line - len(content_lines)
#         end = self.line

#         # end = sum(len(line) for line in lines[:self.line]) + self.column - 1

#         output = []
#         for i, line in zip(range(start, end+1), program_lines[start:end+1]):
#             padding = (len(str(end)) - len(str(i))) * " "
#             output.append(f"{padding}{str(i)} | {line}")

#         return "\n".join(output)
    
#     @classmethod
#     def display(cls, filename, program, e):
#         output = [f"{e}"]

#         output.append(f"In {filename} [{e.line}:{e.column}]:")

#         output.append(e.format_code(program))

#         output.append(cls.congratulations)

#         print("\n".join(output))
    
