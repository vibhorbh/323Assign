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
        self.pos = 0

        # So output printed to show parser processes can be saved to file
        self.process_output = []

        # Initialize the lexer so self.token contains the first token
        # of the source code and self.pos points to the position after it.
        # Parser functions consume tokens by calling self._lexer()
        # after successfully matching the current token.

        self.token = None
        self._lexer()

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
        if self.token is None:
            return None
        return self.token.token

    # Convienence function for getting the current lexeme (token instance).
    # Note the _ at the beginning
    def _lexeme(self):
        if self.token is None:
            return None
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


    
    # R1. <Rat26F> ::= <Opt Function Definitions> @ <Opt Declaration List> @ <Statement List>
    def Rat26F(self):
        self._add_parser_output(
            "<Rat26F> ::= <Opt Function Definitions> @ <Opt Declaration List> @ <Statement List>"
        )

        self.OptFunctionDefinitions()

        # First @
        if self._token() == "separator" and self._lexeme() == "@":
            self._print_token_lexeme()
            self._lexer()
        else:
            self._syntax_error("@")

        # Optional declarations
        self.OptDeclarationList()

        # Second @
        if self._token() == "separator" and self._lexeme() == "@":
            self._print_token_lexeme()
            self._lexer()
        else:
            self._syntax_error("@")

        # Statement list
        self.StatementList()

    # R2. <Opt Function Definitions> ::= <Function Definitions>  |  <Empty>
    def OptFunctionDefinitions(self):
        self._add_parser_output("<Opt Function Definitions> ::= <Function Definitions>  |  <Empty>")
        if (self._token() == "keyword"
                and self._lexeme() == "function"):
            self.FunctionDefinitions()
        else:
            self.Empty()

    # R3. <Function Definitions> ::= <Function> | <Function> <Function Definitions>
    def FunctionDefinitions(self):
        self._add_parser_output("<Function Definitions> ::= <Function> | <Function> <Function Definitions>")
        self.Function()
        if (self._token() == "keyword"
                and self._lexeme() == "function"):
            self.FunctionDefinitions()

    # R4. <Function> ::= function <Identifier> ( <Opt Parameter List> ) <Opt Declaration List> <Body>
    def Function(self):
        self._add_parser_output("<Function> ::= function <Identifier> ( <Opt Parameter List> ) <Opt Declaration List> <Body>")
            # function keyword
        if self._token() == "keyword" and self._lexeme() == "function":
            self._print_token_lexeme()
            self._lexer()
        else:
            self._syntax_error("function")

        # identifier
        if self._token() == "identifier":
            self._print_token_lexeme()
            self._lexer()
        else:
            self._syntax_error("identifier", "Expected function name.")

        # (
        if self._token() == "separator" and self._lexeme() == "(":
            self._print_token_lexeme()
            self._lexer()
        else:
            self._syntax_error("(", "Expected '(' after function name.")

        # optional parameters
        self.OptParameterList()

        # )
        if self._token() == "separator" and self._lexeme() == ")":
            self._print_token_lexeme()
            self._lexer()
        else:
            self._syntax_error(")", "Expected ')' after parameter list.")

        # optional declarations
        self.OptDeclarationList()

        # body
        self.Body()

    # R5. <Opt Parameter List> ::= <Parameter List> | <Empty>
    def OptParameterList(self):
        self._add_parser_output("<Opt Parameter List> ::= <Parameter List> | <Empty>")
        if self._token() == "identifier":
            self.ParameterList()
        else:
            self.Empty()

    # R6. <Parameter List> ::= <Parameter> | <Parameter>, <Parameter List>
    def ParameterList(self):
        self._add_parser_output("<Parameter List> ::= <Parameter> | <Parameter>, <Parameter List>")
        self.Parameter()

        if self._token() == "separator" and self._lexeme() == ",":
            self._print_token_lexeme()
            self._lexer()
            self.ParameterList()

    # R7. <Parameter> ::= <IDs> <Qualifier> 
    def Parameter(self):
        self._add_parser_output("<Parameter> ::= <IDs> <Qualifier> ")
        self.IDs()
        self.Qualifier()

    # R8. <Qualifier> ::= integer | boolean | real
    def Qualifier(self):
        self._add_parser_output("<Qualifier> ::= integer | boolean | real")

        if self._token() == "keyword" and self._lexeme() in ["integer", "boolean", "real"]:
            self._print_token_lexeme()
            self._lexer()
        else:
            self._syntax_error("keyword", "The provided keyword must be 'integer', 'boolean', or 'real'")

    # R9. <Body> ::= {< Statement List >}
    def Body(self):
        self._add_parser_output("<Body> ::= {< Statement List >}")
        if self._token() == "separator" and self._lexeme() == "{":
            self._print_token_lexeme()
            self._lexer()
        else:
            self._syntax_error("separator", "Expected '{'")

        self.StatementList()

        if self._token() == "separator" and self._lexeme() == "}":
            self._print_token_lexeme()
            self._lexer()
        else:
            self._syntax_error("separator", "Expected '}'")

    # R10. <Opt Declaration List> ::= <Declaration List> | <Empty>
    def OptDeclarationList(self):
        self._add_parser_output("<Opt Declaration List> ::= <Declaration List> | <Empty>")
        if (self._token() == "keyword"
                and self._lexeme() in ["integer", "boolean", "real"]):
            self.DeclarationList()
        else:
            self.Empty()

    # R11. <Declaration List>  := <Declaration> ;     |      <Declaration> ; <Declaration List>
    def DeclarationList(self):
        self._add_parser_output("<Declaration List>  := <Declaration> ;     |      <Declaration> ; <Declaration List>")
        self.Declaration()
        if self._token() == "separator" and self._lexeme() == ";":
            self._print_token_lexeme()
            self._lexer()
        else:
            self._syntax_error_missing_semicolon()

        if (self._token() == "keyword"
                and self._lexeme() in ["integer", "boolean", "real"]):
            self.DeclarationList()

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

        if self._token() == "identifier":
            self._print_token_lexeme()
            self._lexer()
        else:
            self._syntax_error("identifier")

        if self._token() == "separator" and self._lexeme() == ",":
            
            self._print_token_lexeme()
            self._lexer()
            self.IDs()

    # R14. <Statement List> ::=   <Statement>   | <Statement> <Statement List>
    def StatementList(self):
        self._add_parser_output(
            "<Statement List> ::= <Statement> | "
            "<Statement> <Statement List>"
        )

        self.Statement()

        while (
                self._token() == "identifier"
                or (
                    self._token() == "separator"
                    and self._lexeme() == "{"
                )
                or (
                    self._token() == "keyword"
                    and self._lexeme() in [
                        "if",
                        "return",
                        "put",
                        "get",
                        "while"
                    ]
                )
            ):
                self.Statement()

    # R15. <Statement> ::= <Compound> | <Assign>
    #       | <If> | <Return> | <Print> | <Scan> | <While>
    def Statement(self):

        if self._token() == "separator" and self._lexeme() == "{":
            self._add_parser_output("<Statement> ::= <Compound>")
            self.Compound()

        elif self._token() == "identifier":
            self._add_parser_output("<Statement> ::= <Assign>")
            self.Assign()

        elif self._token() == "keyword" and self._lexeme() == "if":
            self._add_parser_output("<Statement> ::= <If>")
            self.If()

        elif self._token() == "keyword" and self._lexeme() == "return":
            self._add_parser_output("<Statement> ::= <Return>")
            self.Return()

        elif self._token() == "keyword" and self._lexeme() == "put":
            self._add_parser_output("<Statement> ::= <Print>")
            self._add_parser_output("<Print> ::= put ( <Expression> ) ;")

            # put
            self._print_token_lexeme()
            self._lexer()

            # (
            if self._token() == "separator" and self._lexeme() == "(":
                self._print_token_lexeme()
                self._lexer()
            else:
                self._syntax_error("(")

            # Expression
            self.Expression()

            # )
            if self._token() == "separator" and self._lexeme() == ")":
                self._print_token_lexeme()
                self._lexer()
            else:
                self._syntax_error(")")

            # ;
            if self._token() == "separator" and self._lexeme() == ";":
                self._print_token_lexeme()
                self._lexer()
            else:
                self._syntax_error_missing_semicolon()

        elif self._token() == "keyword" and self._lexeme() == "get":
            self._add_parser_output("<Statement> ::= <Scan>")
            self.Scan()

        elif self._token() == "keyword" and self._lexeme() == "while":
            self._add_parser_output("<Statement> ::= <While>")
            self.While()

        else:
            self._syntax_error("statement")

    # R16. <Compound> ::= { <Statement List> }
    def Compound(self):
        self._add_parser_output(
            "<Compound> ::= { <Statement List> }"
        )

        if self._token() == "separator" and self._lexeme() == "{":
            self._print_token_lexeme()
            self._lexer()
        else:
            self._syntax_error("{")

        self.StatementList()

        if self._token() == "separator" and self._lexeme() == "}":
            self._print_token_lexeme()
            self._lexer()
        else:
            self._syntax_error("}")

    # R17. <Assign> ::= <Identifier> = <Expression> ;
    def Assign(self):
        self._add_parser_output(
            "<Assign> ::= <Identifier> = <Expression> ;"
        )

        # Identifier
        if self._token() == "identifier":
            self._print_token_lexeme()
            self._lexer()
        else:
            self._syntax_error("identifier")

        # =
        if self._token() == "operator" and self._lexeme() == "=":
            self._print_token_lexeme()
            self._lexer()
        else:
            self._syntax_error("=", "Expected assignment operator.")

        # Expression
        self.Expression()

        # ;
        if self._token() == "separator" and self._lexeme() == ";":
            self._print_token_lexeme()
            self._lexer()
        else:
            self._syntax_error_missing_semicolon()

    # R18. <If> ::= if ( <Condition> ) <Statement> <If Prime>
    def If(self):
        self._add_parser_output(
            "<If> ::= if ( <Condition> ) <Statement> <If Prime>"
        )

        # consume if
        if self._token() == "keyword" and self._lexeme() == "if":
            self._print_token_lexeme()
            self._lexer()
        else:
            self._syntax_error("if")

        # (
        if self._token() == "separator" and self._lexeme() == "(":
            self._print_token_lexeme()
            self._lexer()
        else:
            self._syntax_error("(")

        # condition
        self.Condition()

        # )
        if self._token() == "separator" and self._lexeme() == ")":
            self._print_token_lexeme()
            self._lexer()
        else:
            self._syntax_error(")")

        # statement after condition
        self.Statement()

        # optional else/fi
        self.IfPrime()

    # R19. <If Prime> ::= endif | else <Statement> endif
    def IfPrime(self):
        if self._token() == "keyword" and self._lexeme() == "else":
            self._add_parser_output(
                "<If Prime> ::= else <Statement> fi"
            )

            # consume else
            self._print_token_lexeme()
            self._lexer()

            # statement after else
            self.Statement()

            # consume fi
            if self._token() == "keyword" and self._lexeme() == "fi":
                self._print_token_lexeme()
                self._lexer()
            else:
                self._syntax_error("fi")

        elif self._token() == "keyword" and self._lexeme() == "fi":
            self._add_parser_output(
                "<If Prime> ::= fi"
            )

            # consume fi
            self._print_token_lexeme()
            self._lexer()

        else:
            self._syntax_error("fi or else")

    # R20. <Return> ::= return ; | return <Expression> ;
    def Return(self):
        self._add_parser_output(
            "<Return> ::= return ; | return <Expression> ;"
        )

        # return
        if self._token() == "keyword" and self._lexeme() == "return":
            self._print_token_lexeme()
            self._lexer()
        else:
            self._syntax_error("return")

        # empty return: return ;
        if self._token() == "separator" and self._lexeme() == ";":
            self._print_token_lexeme()
            self._lexer()
            return

        # return expression;
        self.Expression()

        if self._token() == "separator" and self._lexeme() == ";":
            self._print_token_lexeme()
            self._lexer()
        else:
            self._syntax_error_missing_semicolon()


    # R21. <Scan> ::= get ( <IDs> );
    def Scan(self):
        self._add_parser_output("<Scan> ::= get ( <IDs> );")

        # get
        if self._token() == "keyword" and self._lexeme() == "get":
            self._print_token_lexeme()
            self._lexer()
        else:
            self._syntax_error("get")

        # (
        if self._token() == "separator" and self._lexeme() == "(":
            self._print_token_lexeme()
            self._lexer()
        else:
            self._syntax_error("(")

        # IDs
        self.IDs()

        # )
        if self._token() == "separator" and self._lexeme() == ")":
            self._print_token_lexeme()
            self._lexer()
        else:
            self._syntax_error(")")

        # ;
        if self._token() == "separator" and self._lexeme() == ";":
            self._print_token_lexeme()
            self._lexer()
        else:
            self._syntax_error_missing_semicolon()


    # R22. <While> ::= while ( <Condition> ) <Statement>
    def While(self):
        self._add_parser_output(
            "<While> ::= while ( <Condition> ) <Statement>"
        )

        # consume while
        if self._token() == "keyword" and self._lexeme() == "while":
            self._print_token_lexeme()
            self._lexer()
        else:
            self._syntax_error("while")

        # (
        if self._token() == "separator" and self._lexeme() == "(":
            self._print_token_lexeme()
            self._lexer()
        else:
            self._syntax_error("(")

        # condition
        self.Condition()

        # )
        if self._token() == "separator" and self._lexeme() == ")":
            self._print_token_lexeme()
            self._lexer()
        else:
            self._syntax_error(")")

        # statement body
        self.Statement()
   # R23. <Condition> ::= <Expression> <Relop> <Expression>
    def Condition(self):
       self._add_parser_output("<Condition> ::= <Expression> <Relop> <Expression>")
       self.Expression()
       self.Relop()
       self.Expression()
   # R24. <Relop> ::= == | != | > | < | <= | >=
    def Relop(self):
        self._add_parser_output("<Relop> ::= == | != | > | < | <= | >=")
        if self._token() == "operator" and self._lexeme() in [
            "==", "!=", ">", "<", "<=", ">="
        ]:
            self._print_token_lexeme()
            self._lexer()
        else:
            self._syntax_error("relational operator")
   # R25. <Expression> ::= <Expression> + <Term> | <Expression> - <Term> | <Term>
    def Expression(self):
        self._add_parser_output("<Expression> ::= <Expression> + <Term> | <Expression> - <Term> | <Term>")
        self.Term()

        if self._token() == "operator" and self._lexeme() in ["+", "-"]:
            self._print_token_lexeme()
            self._lexer()
            self.Expression()

   # R26. <Term> ::= <Term> * <Factor> | <Term> / <Factor> | <Factor>
    def Term(self):
        self._add_parser_output("<Term> ::= <Term> * <Factor> | <Term> / <Factor> | <Factor>")
        self.Factor()
        if self._token() == "operator" and self._lexeme() in ["*", "/"]:
            self._print_token_lexeme()
            self._lexer()
            self.Term()
    
   # R27. <Factor> ::= - <Primary> | <Primary>
    def Factor(self):
        self._add_parser_output("<Factor> ::= - <Primary> | <Primary>")
        if self._token() == "operator" and self._lexeme() == "-":
            self._print_token_lexeme()
            self._lexer()
            self.Primary()
        else:
            self.Primary()
   # R28. <Primary> ::= <Identifier> | <Integer> | <Identifier> ( <IDs> ) | ( <Expression> ) |
    def Primary(self):
        self._add_parser_output(
            "<Primary> ::= <Identifier> | <Integer> | "
            "<Identifier> ( <IDs> ) | ( <Expression> ) | "
            "<Real> | true | false"
        )

        # Identifier or function call
        if self._token() == "identifier":
            self._print_token_lexeme()
            self._lexer()

            # <Identifier> ( <IDs> )
            if self._token() == "separator" and self._lexeme() == "(":
                self._print_token_lexeme()
                self._lexer()

                # Optional IDs (allows empty function calls like foo())
                if not (self._token() == "separator" and self._lexeme() == ")"):
                    self.IDs()

                if self._token() == "separator" and self._lexeme() == ")":
                    self._print_token_lexeme()
                    self._lexer()
                else:
                    self._syntax_error(")")

        # Integer
        elif self._token() == "integer":
            self._print_token_lexeme()
            self._lexer()

        # Real
        elif self._token() == "real":
            self.Real()

        # ( <Expression> )
        elif self._token() == "separator" and self._lexeme() == "(":
            self._print_token_lexeme()
            self._lexer()

            self.Expression()

            if self._token() == "separator" and self._lexeme() == ")":
                self._print_token_lexeme()
                self._lexer()
            else:
                self._syntax_error(")")

        # true | false
        elif self._token() == "keyword" and self._lexeme() in ["true", "false"]:
            self._print_token_lexeme()
            self._lexer()

        else:
            self._syntax_error(
                "identifier, integer, real, true, false, or '('"
            )
   # <Real> | true | false
    def Real(self):
        self._add_parser_output("<Real> ::= <Real>")

        if self._token() == "real":
            self._print_token_lexeme()
            self._lexer()
        else:
            self._syntax_error("real")
   # R29. <Empty> ::= eps
    def Empty(self):
        self._add_parser_output("<Empty> ::= eps")
        # Nothing to do here, as this is an empty production


###########################################################

def _print_usage_and_exit():
    print(f"Usage: {sys.argv[0]} [input file] [output file (optional)] [OPTIONS (optional)]")
    print("\nOptional OPTIONS include:\n\t--save-syntax-error\tWrite output to file even if a syntax error was detected. The syntax error message will be included at the end of the output file.")
    sys.exit(1)

def main():
    if len(sys.argv) < 2 or len(sys.argv) > 4:
        _print_usage_and_exit()

    save_syntax_error = False
    if len(sys.argv) == 4:
        if sys.argv[3] == "--save-syntax-error":
            save_syntax_error = True
        else:
            # If the user wants to specify an optional option for assignment2.py,
            # then currently, the only valid option is --save-syntax-error
            print("Option not recognized.")
            _print_usage_and_exit()

    out_name = sys.argv[2] if len(sys.argv) in [3, 4] else "output.txt"

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

    if save_syntax_error:
        if parser_syntax_error:
            output = f"{output}\n\n{parser_syntax_error.msg}"
    else:
        # If user doesn't want to save the syntax error, do not write to output file if there was a syntax error
        if parser_syntax_error:
            raise parser_syntax_error

    with open(out_name, "w") as out:
        out.write(output + "\n")

    # If there was a syntax error, but the user wanted to save the syntax error to output file, still print error to console.
    if parser_syntax_error:
        raise parser_syntax_error

if __name__ == "__main__":
    main()
