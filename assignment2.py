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
        # This call to lexer() uses the lexer function from assignment1 (see assignment1.py for details)
        self.token, self.pos = lexer(self.source, self.pos)

    # Convenience function, mainly so the coding style matches the one from the assignment instructions
    # (where calls to lexer() made by the RDP functions do not supply parameters and expect the lexer function
    # to move to the next tokens for them)
    # For this to work here, make sure to call "self.lexer()" in the RDP functions instead of just "lexer()"
    # Note the _ at the beginning
    def _lexer(self):
        self.next_token()

    # Convienence function for getting the current token.
    # Note the _ at the beginning
    def _token(self):
        return self.token.token

    # Convienence function for getting the current lexeme (token instance).
    # Note the _ at the beginning
    def _lexeme(self):
        return self.token.lexeme

    def _print_token_lexeme(self):
        print(print(f"Token: {self._token():<16}Lexeme: {self._lexeme()}"))

    def _syntax_error(self, expected_token, additional_info=""):
        # TODO: Figure out how to get line numbers displayed in the error
        raise SyntaxError(f"Syntax error while parsing source code at character #{self.pos}\n\tExpected token: {expected_token}\n\tGot this token instead:\n\t: {self._token()}\n\tWith this lexeme: {self._lexeme()}\n{additional_info}")
    
    # R1. <Rat26F>  ::=   <Opt Function Definitions>   @  <Opt Declaration List> @  <Statement List>
    # R1 doesn't need to be coded

    # R2. <Opt Function Definitions> ::= <Function Definitions>  |  <Empty>
    def OptFunctionDefinitions(self):
        print("<Opt Function Definitions> ::= <Function Definitions>  |  <Empty>")
        self.FunctionDefinitions()

    # R3. <Function Definitions> ::= <Function> | <Function> <Function Definitions>
    def FunctionDefinitions(self):
        print("<Function Definitions> ::= <Function> | <Function> <Function Definitions>")
        self.Function()

    # R4. <Function> ::= function <Identifier> ( <Opt Parameter List> ) <Opt Declaration List> <Body>
    def Function(self):
        print("<Function> ::= function <Identifier> ( <Opt Parameter List> ) <Opt Declaration List> <Body>")
        if self._token() == "keyword" and self._lexeme() == "function":
            self._print_token_lexeme()
            self._lexer()
            if self._token() == "separator" and self._lexeme() == "(":
                self._print_token_lexeme()
                self.OptParameterList()
            else:
                self._syntax_error("separator", "Expected '(' after function name.")

            self._lexer()
            if self._token() == "separator" and self._lexeme() == ")":
                self._print_token_lexeme()
                self.OptDeclarationList()
            else:
                self._syntax_error("separator", "Expected ')' after parameter or parameter list.")

    # R5. <Opt Parameter List> ::= <Parameter List> | <Empty>
    def OptParameterList(self):
        print("<Opt Parameter List> ::= <Parameter List> | <Empty>")
        self.ParameterList()

    # R6. <Parameter List> ::= <Parameter> | <Parameter>, <Parameter List>
    def ParameterList(self):
        print("<Parameter List> ::= <Parameter> | <Parameter>, <Parameter List>")
        self.Parameter()

    # R7. <Parameter> ::= <IDs> <Qualifier> 
    def Parameter(self):
        print("<Parameter> ::= <IDs> <Qualifier> ")
        self._lexer()
        if self._token() == "identifier":
            self._print_token_lexeme()
            self.Qualifier()
        else:
            self._syntax_error("identifier")

    # R8. <Qualifier> ::= integer | boolean | real
    def Qualifier(self):
        print("<Qualifier> ::= integer | boolean | real")
        self._lexer()
        if self._token() == "keyword" and self._lexeme() in ["integer", "boolean", "real"]:
            self._print_token_lexeme()
        else:
            self._syntax_error("keyword", "The provided keyword must be 'integer', 'boolean', or 'real'")

    # R9. <Body> ::= {< Statement List >}
    def Body(self):
        print("<Body> ::= {< Statement List >}")

    # R10. <Opt Declaration List> ::= <Declaration List> | <Empty>
    def OptDeclarationList(self):
        print("<Opt Declaration List> ::= <Declaration List> | <Empty>")

    # R11. <Declaration List>  := <Declaration> ;     |      <Declaration> ; <Declaration List>
    def DeclarationList(self):
        print("<Declaration List>  := <Declaration> ;     |      <Declaration> ; <Declaration List>")


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
