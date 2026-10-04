# CPSC323 Assignment 1
# Rat26F Lexical Analyzer
# By Simone Bacani, Vibhor Bhargava, Aaron Yu

import sys
from collections import namedtuple

# A token record: one field for the token type, one for the lexeme
Token = namedtuple("Token", ["token", "lexeme"])

DIGITS = "0123456789"
LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

KEYWORDS = {
    "function", "integer", "boolean", "real", "if", "else", "fi",
    "while", "return", "get", "put", "true", "false",
}
SEPARATORS = set("(){},;@")
TWO_CHAR_OPERATORS = {"==", "!=", "<=", ">="}
ONE_CHAR_OPERATORS = set("=+-*/<>")


# ---------------------------------------------------------------------------
# Deterministic finite state machines (DFSMs)
# Each DFSM is a dict with a start state, a set of accepting states, and a
# transition table mapping (state, input class) -> next state.
# A missing entry means "dead state" (no valid transition).
# ---------------------------------------------------------------------------

def char_class(ch):
    """Map a character to the input class used by the DFSM tables."""
    if ch in DIGITS:
        return "digit"
    if ch in LETTERS:
        return "letter"
    if ch == "_":
        return "underscore"
    if ch == ".":
        return "dot"
    return "other"


# Identifier RE: letter (letter | digit | _)*
IDENTIFIER_DFSM = {
    "start": 0,
    "accepting": {1},
    "table": {
        (0, "letter"): 1,
        (1, "letter"): 1,
        (1, "digit"): 1,
        (1, "underscore"): 1,
    },
}

# Integer RE: digit+
INTEGER_DFSM = {
    "start": 0,
    "accepting": {1},
    "table": {
        (0, "digit"): 1,
        (1, "digit"): 1,
    },
}

# Real RE: digit* . digit+      (e.g. 123.00 or .001, but NOT 123.)
REAL_DFSM = {
    "start": 0,
    "accepting": {3},
    "table": {
        (0, "digit"): 1,
        (0, "dot"): 2,
        (1, "digit"): 1,
        (1, "dot"): 2,
        (2, "digit"): 3,
        (3, "digit"): 3,
    },
}


def run_dfsm(dfsm, text, pos):
    """
    Runs the DFSM starting at the given position.
    Returns where the longest valid match ends,
    or -1 if nothing matched.
    """
    state = dfsm["start"]
    last_accept = -1
    i = pos
    while i < len(text):
        nxt = dfsm["table"].get((state, char_class(text[i])))
        if nxt is None:
            break
        state = nxt
        i += 1
        if state in dfsm["accepting"]:
            last_accept = i
    return last_accept


# ---------------------------------------------------------------------------
# The lexer
# ---------------------------------------------------------------------------

def skip_whitespace(text, pos):
    """
    Skips spaces, new lines, tabs, and comments (! ... !).
    Returns the new position, or an error if a comment
    was never closed.
    """
    n = len(text)
    while pos < n:
        ch = text[pos]
        if ch in " \t\r\n":
            pos += 1
        elif ch == "!" and text[pos:pos + 2] != "!=":
            # Comment: skip to the closing '!'
            end = text.find("!", pos + 1)
            if end == -1:
                return n, "unterminated comment"
            pos = end + 1
        else:
            break
    return pos, None


def lexer(text, pos):
    """
    Returns the next token starting at pos.
    Returns None when the end of the file is reached.
    """
    pos, error = skip_whitespace(text, pos)
    if error:
        return Token("error", error), len(text)
    if pos >= len(text):
        return None, pos

    ch = text[pos]

    # Identifiers / keywords (case-insensitive)
    if ch in LETTERS:
        end = run_dfsm(IDENTIFIER_DFSM, text, pos)
        lexeme = text[pos:end]
        if lexeme.lower() in KEYWORDS:
            return Token("keyword", lexeme), end
        return Token("identifier", lexeme), end

    # Numbers: try real first (it is the more specific pattern), then integer
    if ch in DIGITS or ch == ".":
        end = run_dfsm(REAL_DFSM, text, pos)
        if end != -1:
            return Token("real", text[pos:end]), end
        end = run_dfsm(INTEGER_DFSM, text, pos)
        if end != -1:
            return Token("integer", text[pos:end]), end
        # A lone '.' (or similar) falls through to "unknown" below

    # Operators (check two-character ones first)
    if text[pos:pos + 2] in TWO_CHAR_OPERATORS:
        return Token("operator", text[pos:pos + 2]), pos + 2
    if ch in ONE_CHAR_OPERATORS:
        return Token("operator", ch), pos + 1

    # Separators
    if ch in SEPARATORS:
        return Token("separator", ch), pos + 1

    # Anything else is not part of Rat26F
    return Token("unknown", ch), pos + 1


def main():
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: assignment1.py [input file] [output file (optional)]")
        sys.exit(1)

    out_name = sys.argv[2] if len(sys.argv) == 3 else "output.txt"

    # Read the whole file at once, since comments can span several lines
    with open(sys.argv[1]) as f:
        source = f.read()

    lines = [f"{'token':<12}lexeme"]
    pos = 0
    while True:
        tok, pos = lexer(source, pos)
        if tok is None:
            break
        lines.append(f"{tok.token:<12}{tok.lexeme}")

    output = "\n".join(lines)
    print(output)
    with open(out_name, "w") as out:
        out.write(output + "\n")


if __name__ == "__main__":
    main()