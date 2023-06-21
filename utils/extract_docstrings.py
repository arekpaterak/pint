import re

def extract_docstrings(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()

    docstrings = re.findall(r'"""(.*?)"""', content, re.DOTALL)
    return docstrings


filename = 'tokens_and_grammar.py'
docstrings = extract_docstrings(filename)

for docstring in docstrings:
    print(docstring, end='')
