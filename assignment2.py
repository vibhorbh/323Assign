# CPSC323 Assignment 2
# Rat26F Syntax Analyzer
# By Simone Bacani, Vibhor Bhargava, Aaron Yu

from assignment1 import lexer, Token
import sys


### PRODUCTION RULES CODED AS RECURSIVE DESCENT PARSERS ###

# For all of the rules coded as RDP functions,
# the parameter 'tok' is a Token instance with the following
# variables:
# tok.token: The token type. (ex. token type for myVar is 'identifier')
# tok.lexeme: The actual token instance (ex. 'myVar')

# tok.token and tok.lexeme are always strings.
# See assignment1.py for the full definition of the Token class.

class Rat26F_RDP:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def _current(self):
        return self.tokens[self.pos]

    def _eof(self):
        return self._current().token == 'EOF'

    def _next(self):
        if not self._eof():
            self.pos += 1


    # R1. <Rat26F>  ::=   <Opt Function Definitions>   @  <Opt Declaration List> @  <Statement List>
    # R1 doesn't need to be coded

    # R2. <Opt Function Definitions> ::= <Function Definitions>  |  <Empty>
    def OptFunctionDefinitions(self):
        pass


###########################################################

def main():
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print(f"Usage: {sys.argv[0]} [input file] [output file (optional)]")
        sys.exit(1)

    # Read the whole file at once, since comments can span several lines
    with open(sys.argv[1]) as f:
        source = f.read()

    tokens = []
    pos = 0
    while True:
        tok, pos = lexer(source, pos)
        if tok is None:
            break

        tokens.append(tok)

    # This is needed so the recursive descent parser knows where to stop
    tokens.append(Token('EOF', None))

if "__name__" == "__main__":
    main()
