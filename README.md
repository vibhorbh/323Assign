# CPSC 323 Assignment 1: Rat26F Lexical Analyzer

**Authors:** Simone Bacani, Vibhor Bhargava, Aaron Yu
**Course:** CPSC 323, Fall 2026

## Overview

This program is a lexical analyzer (lexer) for the Rat26F language. It reads a
Rat26F source file, breaks it into tokens, and writes each token and its lexeme to an output file (and to the terminal).

Identifiers, integers, and reals are recognized with deterministic finite state machines (DFSMs) driven by transition tables. Operators, separators, and
keywords are handled via set lookups.

## How to run

For teammates:

```
python assignment1.py <input file> [output file]
```

- `<input file>`: the Rat26F source file to analyze.
- `[output file]`: optional. If omitted, results are written to `output.txt`.

Example:

```
python assignment1.py input1.txt output1.txt
```

If you are using the executable instead of Python, run it the same way:

```
assignment1.exe tests/test1.txt tests/output1.txt     (Windows)
./assignment1 tests/test1.txt tests/output1.txt       (Linux)
```

Running with the wrong number of arguments prints a usage message and exits.

## Output format

The output has a header line followed by one line per token:

```
token       lexeme
keyword     while
separator   (
identifier  fahr
operator    <=
real        23.00
```

### Token types

| Token        | Description                                                        |
|--------------|--------------------------------------------------------------------|
| `keyword`    | function, integer, boolean, real, if, else, fi, while, return, get, put, true, false |
| `identifier` | A letter followed by letters, digits, or `_`                       |
| `integer`    | One or more digits                                                 |
| `real`       | Optional digits, a `.`, then one or more digits (e.g. `23.00`, `.001`) |
| `operator`   | `==  !=  <=  >=  =  +  -  *  /  <  >`                              |
| `separator`  | `( ) { } , ; @`                                                    |
| `unknown`    | Any character that is not part of Rat26F (e.g. `#`)                |
| `error`      | An unterminated comment (comment opened with `!` but never closed) |

## Design

### Regular expressions

| Token      | Regular expression              |
|------------|---------------------------------|
| Identifier | `letter (letter \| digit \| _)*` |
| Integer    | `digit+`                        |
| Real       | `digit* . digit+`               |

### DFSMs

Each DFSM is stored as a dictionary containing a start state, a set of
accepting states, and a transition table keyed by `(state, character class)`.
A missing table entry means the machine has hit a dead state.

`run_dfsm()` is shared by all three machines. It runs a machine over the input
starting at the current position and returns the end of the **longest** accepted
lexeme (or -1 if nothing was accepted).

- **Identifier DFSM:** 2 states. State 0 goes to state 1 on a letter; state 1
  loops on a letter, digit, or `_`. Accepting state: 1.
- **Integer DFSM:** 2 states. State 0 goes to state 1 on a digit; state 1 loops
  on a digit. Accepting state: 1.
- **Real DFSM:** 4 states. State 0 goes to 1 on a digit or to 2 on `.`; state 1
  loops on a digit or goes to 2 on `.`; state 2 goes to 3 on a digit; state 3
  loops on a digit. Accepting state: 3.

### How `lexer()` works

`lexer(text, pos)` returns a `Token(token, lexeme)` record and the new position
in the source (or `None` at end of input). The main program calls it in a loop
until the end of the file:

1. Skip white space and comments (`! ... !`).
2. If the next character is a letter, run the identifier DFSM, then check
   whether the lexeme is a keyword (case-insensitive).
3. If the next character is a digit or `.`, try the real DFSM first, then the
   integer DFSM.
4. Otherwise check for a two-character operator, a one-character operator, or a
   separator.
5. Anything else is returned as an `unknown` token.

## Notes and limitations

- **Comments** are enclosed in `! !` and may span multiple lines. They are
  skipped entirely and produce no tokens.
- **`!=` vs. comments:** `!` starts a comment unless it is immediately followed
  by `=`, in which case it is read as the `!=` operator. A comment that begins
  with `!=` is therefore misread.
- **Case:** Keywords are matched case-insensitively (`WHILE` is a keyword).
  Lexemes are printed exactly as written in the source.
- **`123.`** is not a valid real, so it is read as the integer `123` followed by
  an `unknown` token for the `.`.
- **`.5x`** is read as the real `.5` followed by the identifier `x`.
- The lexer only performs lexical analysis. It does not check syntax or
  semantics.

## Files

```
assignment1.py      Lexer source code
README.md           This file
tests/
    test1.txt       Test case 1 (under 10 lines)
    output1.txt     Output for test 1
    test2.txt       Test case 2 (under 21 lines, project sample program)
    output2.txt     Output for test 2
    test3.txt       Test case 3 (over 21 lines, edge cases)
    output3.txt     Output for test 3
```