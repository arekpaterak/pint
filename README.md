# Pint 🍺
A programming language brewed 🍺 with love ❤ and the finest emojis 😀

## The language 
Pint is a statically typed programming language using emojis as keywords with a syntax inspired by Python (with some twists).

## The transpiler
Pint's transpiler is called **Debrewer**. Its output is **Python**.

It is implemented in **Python** and uses **PLY** (Python Lex-Yacc) to tokenize and parse the input file.

### How to use
To transpile a Pint file to python, run `python debrewer.py <input> [-o <output>] [-t]`. 

Without specifying flags the result will be saved in a file with the same name as the input file, but with the `.py` extension. 
The `-o` flag specifies the output file, and the `-t` flag specifies that the output should be printed to the terminal. 

### Testing
Simple tests compare translated files to model ones from the examples directory.

Use: `python -m unittest`
