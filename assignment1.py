# CPSC323 Assignment 1
# Rat26F Lexical Analyzer
# By Simone Bacani, Vibhor Bhargava, Aaron Yu

import sys

def lexer(f):
    """
    Given a file f containing Rat26F source code,
    print every token and its corresponding
    lexeme (token instance). 
    """

    while True:
        line = f.readline()

        # Empty string = EOF
        if not line:
            break

        # TODO: Parse line and scan for tokens


if __name__ == "main":
    if len(sys.argv) != 2:
        print("Usage: assignment1.py [input file]")

    with open(sys.argv[1]) as f: lexer(f)
