# CPSC323 Assignment 2
# Rat26F Syntax Analyzer
# By Simone Bacani, Vibhor Bhargava, Aaron Yu

from assignment1 import lexer
import sys


### PRODUCTION RULES CODED AS RECURSIVE DESCENT PARSERS ###

class Rat26F_RDP:
    def __init__(self, source):
        self.source = source
        self.pos = 0

        # lexer function returns an incremented pos that can be used to overwrite
        # our current value of pos
        # We ignore the returned pos here so the first token is assigned position 0
        tok, _ = lexer(source, 0)
        self.token = tok

    def next_token(self):
        self.token, self.pos = lexer(self.source, self.pos)

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

    parser = Rat26F_RDP(source)
    while parser.token != None:
        print(f"Token: {parser.token.token:<16}Lexeme: {parser.token.lexeme}")
        parser.next_token() # For testing, modify/remove later

if __name__ == "__main__":
    main()
