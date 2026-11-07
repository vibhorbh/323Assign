# CPSC323 Assignment 2
# Rat26F Syntax Analyzer
# By Simone Bacani, Vibhor Bhargava, Aaron Yu

from assignment1 import lexer
import sys


### PRODUCTION RULES CODED AS RECURSIVE DESCENT PARSER FUNCTIONS ###
class Rat26F_RDP:
    """Syntax analyzer for the Rat26F programming language. Implemented as a Recursive Descent Parser class."""
    def __init__(self, source):
        self.source = source
        self.pos = -1

        # So output printed to show parser processes can be saved to file
        self.process_output = []

        # lexer function returns an incremented pos that can be used to overwrite
        # our current value of pos
        # We ignore the returned pos here so the first token is assigned position 0
        # tok, _ = lexer(source, 0)
        # self.token = tok

        self.token = None

    def parse(self):
        """Parses the source code that was used to create this Rat26F_RDP instance."""
        self.Rat26F()

    # Convenience function, mainly so the coding style matches the one from the assignment instructions
    # (where calls to lexer() made by the RDP functions do not supply parameters and expect the lexer function
    # to move to the next tokens for them)
    # For this to work here, make sure to call "self.lexer()" in the RDP functions instead of just "lexer()"
    # Note the _ at the beginning
    def _lexer(self):
        # This call to lexer() uses the lexer function from assignment1 (see assignment1.py for details)
        self.token, self.pos = lexer(self.source, self.pos)

    # Convienence function for getting the current token.
    # Note the _ at the beginning
    def _token(self):
        return self.token.token

    # Convienence function for getting the current lexeme (token instance).
    # Note the _ at the beginning
    def _lexeme(self):
        return self.token.lexeme

    def _add_parser_output(self, text):
        self.process_output.append(text)

    def _print_token_lexeme(self):
        self._add_parser_output(f"Token: {self._token():<16}Lexeme: {self._lexeme()}")

    def _syntax_error(self, expected_token, additional_info=""):
        # TODO: Figure out how to get line numbers displayed in the error
        raise SyntaxError(f"Syntax error while parsing source code at character #{self.pos}\n\tExpected token: {expected_token}\n\tGot this token instead: {self._token()}\n\tWith this lexeme: {self._lexeme()}\n{additional_info}")

    def _syntax_error_missing_semicolon(self):
        # TODO: Figure out how to get line numbers displayed in the error
        raise SyntaxError(f"Syntax error while parsing source code at character #{self.pos}. Missing ';'")


    
    # R1. <Rat26F>  ::=   <Opt Function Definitions>   @  <Opt Declaration List> @  <Statement List>
    def Rat26F(self):
        self._add_parser_output("<Rat26F>  ::=   <Opt Function Definitions>   @  <Opt Declaration List> @  <Statement List>")
        self.OptFunctionDefinitions()

        self._lexer()
        if self._token() == "separator" and self._lexeme() == "@":
            self._print_token_lexeme()
            self.OptDeclarationList()

            if self._token() == "separator" and self._lexeme() == "@":
                self._print_token_lexeme()

                # Uncomment this after the RDP function for StatementList (rule 14) has been implemented
                # self.StatementList()

            else:
                raise SyntaxError(f"Syntax error while parsing source code at character #{self.pos}. Expected '@', got '{self._lexeme()}'")
        else:
            raise SyntaxError(f"Syntax error while parsing source code at character #{self.pos}. Expected '@', got '{self._lexeme()}'")

    # R2. <Opt Function Definitions> ::= <Function Definitions>  |  <Empty>
    def OptFunctionDefinitions(self):
        self._add_parser_output("<Opt Function Definitions> ::= <Function Definitions>  |  <Empty>")
        self.FunctionDefinitions()

    # R3. <Function Definitions> ::= <Function> | <Function> <Function Definitions>
    def FunctionDefinitions(self):
        self._add_parser_output("<Function Definitions> ::= <Function> | <Function> <Function Definitions>")
        self.Function()

    # R4. <Function> ::= function <Identifier> ( <Opt Parameter List> ) <Opt Declaration List> <Body>
    def Function(self):
        self._add_parser_output("<Function> ::= function <Identifier> ( <Opt Parameter List> ) <Opt Declaration List> <Body>")
        self._lexer()
        if self._token() == "keyword" and self._lexeme() == "function":
            self._print_token_lexeme()

            self._lexer()
            if self._token() == "identifier":
                self._print_token_lexeme()
            else:
                self._syntax_error("identifier", "Did you forget to name the function?")

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
        self._add_parser_output("<Opt Parameter List> ::= <Parameter List> | <Empty>")
        self.ParameterList()

    # R6. <Parameter List> ::= <Parameter> | <Parameter>, <Parameter List>
    def ParameterList(self):
        self._add_parser_output("<Parameter List> ::= <Parameter> | <Parameter>, <Parameter List>")
        self.Parameter()

    # R7. <Parameter> ::= <IDs> <Qualifier> 
    def Parameter(self):
        self._add_parser_output("<Parameter> ::= <IDs> <Qualifier> ")
        self._lexer()
        if self._token() == "identifier":
            self._print_token_lexeme()
            self.Qualifier()
        else:
            self._syntax_error("identifier")

    # R8. <Qualifier> ::= integer | boolean | real
    def Qualifier(self):
        self._add_parser_output("<Qualifier> ::= integer | boolean | real")
        self._lexer()
        if self._token() == "keyword" and self._lexeme() in ["integer", "boolean", "real"]:
            self._print_token_lexeme()
        else:
            self._syntax_error("keyword", "The provided keyword must be 'integer', 'boolean', or 'real'")

    # R9. <Body> ::= {< Statement List >}
    def Body(self):
        self._add_parser_output("<Body> ::= {< Statement List >}")

    # R10. <Opt Declaration List> ::= <Declaration List> | <Empty>
    def OptDeclarationList(self):
        self._add_parser_output("<Opt Declaration List> ::= <Declaration List> | <Empty>")
        self.DeclarationList()

    # R11. <Declaration List>  := <Declaration> ;     |      <Declaration> ; <Declaration List>
    def DeclarationList(self):
        self._add_parser_output("<Declaration List>  := <Declaration> ;     |      <Declaration> ; <Declaration List>")
        self.Declaration()
        self._lexer()
        if self._token() == "separator" and self._lexeme() == ";":
            self._print_token_lexeme()
            return
        else:
            self._syntax_error_missing_semicolon()

    # R12. <Declaration> ::=   <Qualifier> <IDs>
    def Declaration(self):
        # TODO: implement
        pass


###########################################################

def main():
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print(f"Usage: {sys.argv[0]} [input file] [output file (optional)]")
        sys.exit(1)

    out_name = sys.argv[2] if len(sys.argv) == 3 else "output.txt"

    # Read the whole file at once, since comments can span several lines
    with open(sys.argv[1]) as f:
        source = f.read()

    parser = Rat26F_RDP(source)
    # while parser.token != None:
    #     print(f"Token: {parser.token.token:<16}Lexeme: {parser.token.lexeme}")
    #     parser.next_token() # For testing, modify/remove later

    parser_syntax_error = None
    try:
        parser.parse()
    except SyntaxError as e:
        parser_syntax_error = e

    output = "\n".join(parser.process_output)
    print(output)

    # Do not write to output file if there was a syntax error
    if parser_syntax_error:
        raise parser_syntax_error

    with open(out_name, "w") as out:
        out.write(output + "\n")

if __name__ == "__main__":
    main()
