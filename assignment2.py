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

    def _syntax_error_current_pos(self):
        return f"Syntax error while parsing source code at character #{self.pos}."

    def _syntax_error(self, expected_token, additional_info=""):
        # TODO: Figure out how to get line numbers displayed in the error
        raise SyntaxError(f"{self._syntax_error_current_pos()}\n\tExpected token: {expected_token}\n\tGot this token instead: {self._token()}\n\tWith this lexeme: {self._lexeme()}\n{additional_info}")

    def _syntax_error_missing_semicolon(self):
        # TODO: Figure out how to get line numbers displayed in the error
        raise SyntaxError(f"{self._syntax_error_current_pos()} Missing ';'")


    
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
                self.StatementList()
            else:
                raise SyntaxError(f"{self._syntax_error_current_pos()} Expected '@', got '{self._lexeme()}'")
        else:
            raise SyntaxError(f"{self._syntax_error_current_pos()} Expected '@', got '{self._lexeme()}'")

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

        # Need to peek at the next token and see if it's the ',' separator without moving the RDP's current position
        # so other RDP functions get the correct current position.
        token_ahead, _ = lexer(self.source, self.pos)
        if token_ahead.token == "separator" and token_ahead.lexeme == ",":
            self.ParameterList()

    # R7. <Parameter> ::= <IDs> <Qualifier> 
    def Parameter(self):
        self._add_parser_output("<Parameter> ::= <IDs> <Qualifier> ")
        self.IDs()
        self.Qualifier()

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
        self._lexer()
        if self._token() == "separator" and self._lexeme() == "{":
            self._print_token_lexeme()
            self.StatementList()

            self._lexer()
            if self._token() == "separator" and self._lexeme() == "}":
                self._print_token_lexeme()
                return
            else:
                raise SyntaxError(f"{self._syntax_error_current_pos()} Expected '{'}'}' to end function body.")
        else:
            raise SyntaxError(f"{self._syntax_error_current_pos()} Expected '{'{'}' to begin function body.")

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
        self._add_parser_output(
            "<Declaration> ::= <Qualifier> <IDs>"
        )

        self.Qualifier()
        self.IDs()

    # R13. <IDs> ::=     <Identifier>    | <Identifier>, <IDs>
    def IDs(self):
        self._add_parser_output(
            "<IDs> ::= <Identifier> | <Identifier>, <IDs>"
        )

        self._lexer()

        if self._token() == "identifier":
            self._print_token_lexeme()
        else:
            self._syntax_error("identifier")

        # Check for another identifier after a comma
        next_token = self._peek()

        if (next_token is not None
                and next_token.token == "separator"
                and next_token.lexeme == ","):

            self._lexer()
            self._print_token_lexeme()
            self.IDs()

    # R14. <Statement List> ::=   <Statement>   | <Statement> <Statement List>
    def StatementList(self):
        self._add_parser_output(
            "<Statement List> ::= <Statement> | "
            "<Statement> <Statement List>"
        )

        self.Statement()

        # Continue while another statement begins
        while True:
            next_token = self._peek()

            if next_token is None:
                break

            if (next_token.token == "identifier"
                    or next_token.lexeme in [
                        "{", "if", "return", "put",
                        "get", "while"
                    ]):
                self.Statement()
            else:
                break

    # R15. <Statement> ::= <Compound> | <Assign>
    #       | <If> | <Return> | <Print> | <Scan> | <While>
    def Statement(self):
        next_token = self._peek()

        if next_token is None:
            self._syntax_error("statement")

        if (next_token.token == "separator"
                and next_token.lexeme == "{"):
            self._add_parser_output(
                "<Statement> ::= <Compound>"
            )
            self.Compound()

        elif next_token.token == "identifier":
            self._add_parser_output(
                "<Statement> ::= <Assign>"
            )
            self.Assign()

        elif next_token.lexeme == "if":
            self._add_parser_output(
                "<Statement> ::= <If>"
            )
            self.If()

        elif next_token.lexeme == "return":
            self._add_parser_output(
                "<Statement> ::= <Return>"
            )
            self.Return()

        elif next_token.lexeme == "put":
            self._add_parser_output(
                "<Statement> ::= <Print>"
            )
            self.Print()

        elif next_token.lexeme == "get":
            self._add_parser_output(
                "<Statement> ::= <Scan>"
            )
            self.Scan()

        elif next_token.lexeme == "while":
            self._add_parser_output(
                "<Statement> ::= <While>"
            )
            self.While()

        else:
            self._syntax_error("statement")

    # R16. <Compound> ::= { <Statement List> }
    def Compound(self):
        self._add_parser_output(
            "<Compound> ::= { <Statement List> }"
        )

        self._lexer()

        if self._token() == "separator" and self._lexeme() == "{":
            self._print_token_lexeme()
        else:
            self._syntax_error("separator", "Expected '{'")

        self.StatementList()

        self._lexer()

        if self._token() == "separator" and self._lexeme() == "}":
            self._print_token_lexeme()
        else:
            self._syntax_error("separator", "Expected '}'")

    # R17. <Assign> ::= <Identifier> = <Expression> ;
    def Assign(self):
        self._add_parser_output(
            "<Assign> ::= <Identifier> = <Expression> ;"
        )

        self._lexer()

        if self._token() == "identifier":
            self._print_token_lexeme()
        else:
            self._syntax_error("identifier")

        self._lexer()

        if self._token() == "operator" and self._lexeme() == "=":
            self._print_token_lexeme()
        else:
            self._syntax_error("operator", "Expected '='")

        self.Expression()

        self._lexer()

        if self._token() == "separator" and self._lexeme() == ";":
            self._print_token_lexeme()
        else:
            self._syntax_error_missing_semicolon()

    # R18. <If> ::= if ( <Condition> ) <Statement> <If Prime>
    def If(self):
        self._add_parser_output(
            "<If> ::= if ( <Condition> ) <Statement> <If Prime>"
        )

        self._lexer()

        if self._lexeme() == "if":
            self._print_token_lexeme()
        else:
            self._syntax_error("keyword", "Expected 'if'")

        self._lexer()

        if self._lexeme() == "(":
            self._print_token_lexeme()
        else:
            self._syntax_error("separator", "Expected '('")

        self.Condition()

        self._lexer()

        if self._lexeme() == ")":
            self._print_token_lexeme()
        else:
            self._syntax_error("separator", "Expected ')'")

        self.Statement()
        self.IfPrime()

    # R19. <If Prime> ::= endif | else <Statement> endif
    def IfPrime(self):
        next_token = self._peek()

        if next_token is None:
            self._syntax_error("endif or else")

        if next_token.lexeme == "else":
            self._add_parser_output(
                "<If Prime> ::= else <Statement> endif"
            )

            self._lexer()
            self._print_token_lexeme()

            self.Statement()

            self._lexer()

            if self._lexeme() == "endif":
                self._print_token_lexeme()
            else:
                self._syntax_error("keyword", "Expected 'endif'")

        elif next_token.lexeme == "endif":
            self._add_parser_output(
                "<If Prime> ::= endif"
            )

            self._lexer()
            self._print_token_lexeme()

        else:
            self._syntax_error("endif or else")

    # R20. <Return> ::= return ; | return <Expression> ;
    def Return(self):
        self._lexer()

        if self._lexeme() == "return":
            self._print_token_lexeme()
        else:
            self._syntax_error("keyword", "Expected 'return'")

        next_token = self._peek()

        if next_token is not None and next_token.lexeme == ";":
            self._add_parser_output(
                "<Return> ::= return ;"
            )

        else:
            self._add_parser_output(
                "<Return> ::= return <Expression> ;"
            )
            self.Expression()

        self._lexer()

        if self._token() == "separator" and self._lexeme() == ";":
            self._print_token_lexeme()


    #rule 21


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
