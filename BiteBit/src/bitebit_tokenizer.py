# -----------------------------------------------------------------------------------------------------
# BiteBit Language - Tokenizer / Lexer
# CMPSC 470 | Final Project
#
# This module breaks a BiteBit source string into tokens.
# Each token is a tuple: (token_type, lexeme, line_number)
# -----------------------------------------------------------------------------------------------------

import re

# Reserved words, types, operators, and symbols
RESERVED_WORDS = {"let", "fn", "return", "if", "else", "while", "true", "false", "null", "print"}
DATA_TYPES     = {"Int", "Bool", "String", "Null"}
OPERATORS      = ["==", "!=", "<=", ">=", "<<", ">>", "&&", "||",
                  "+", "-", "*", "/", "%", "=", "<", ">", "!", "&", "|", "^", "~"]
SYMBOLS        = [":", ";", ",", "(", ")", "{", "}"]


class TokenizeError(Exception):
    """Raised when the tokenizer finds something it cannot handle."""
    pass


def tokenize(source_code):
    """
    Takes a BiteBit source string and returns a list of tokens.
    Each token is a tuple: (token_type, lexeme, line_number)
    """
    all_tokens = []
    lines = source_code.split("\n")

    for line_number, line in enumerate(lines, start=1):
        line = line.strip()

        if not line:
            continue

        # Skip full-line comments
        if line.startswith("//"):
            continue

        # Strip inline comments
        if "//" in line:
            line = line.split("//")[0].strip()

        if not line:
            continue

        # We process by scanning character by character using regex patterns.
        # Order matters: longer / more specific patterns come first.
        pos = 0
        while pos < len(line):
            # Skip whitespace
            if line[pos].isspace():
                pos += 1
                continue

            matched = False

            # String literal
            m = re.match(r'"[^"\\]*(?:\\.[^"\\]*)*"', line[pos:])
            if m:
                all_tokens.append(("STRING", m.group(0), line_number))
                pos += len(m.group(0))
                matched = True

            # Hex literal (must come before INT)
            if not matched:
                m = re.match(r'0x[0-9A-Fa-f]+', line[pos:])
                if m:
                    all_tokens.append(("HEX_LITERAL", m.group(0), line_number))
                    pos += len(m.group(0))
                    matched = True

            # Binary literal (must come before INT)
            if not matched:
                m = re.match(r'0b[01]+', line[pos:])
                if m:
                    all_tokens.append(("BINARY_LITERAL", m.group(0), line_number))
                    pos += len(m.group(0))
                    matched = True

            # Integer literal
            if not matched:
                m = re.match(r'\d+', line[pos:])
                if m:
                    all_tokens.append(("INT_LITERAL", m.group(0), line_number))
                    pos += len(m.group(0))
                    matched = True

            # Two-character operators (check before single-char)
            if not matched:
                two = line[pos:pos+2]
                if two in ("==", "!=", "<=", ">=", "<<", ">>", "&&", "||"):
                    all_tokens.append(("OPERATOR", two, line_number))
                    pos += 2
                    matched = True

            # Single-character operators and symbols
            if not matched:
                one = line[pos]
                if one in ("+", "-", "*", "/", "%", "<", ">", "!", "&", "|", "^", "~"):
                    # Special case: = is assignment operator
                    all_tokens.append(("OPERATOR", one, line_number))
                    pos += 1
                    matched = True
                elif one == "=":
                    all_tokens.append(("OPERATOR", one, line_number))
                    pos += 1
                    matched = True
                elif one in (":", ";", ",", "(", ")", "{", "}"):
                    all_tokens.append(("SYMBOL", one, line_number))
                    pos += 1
                    matched = True

            # Identifier, keyword, or data type
            if not matched:
                m = re.match(r'[A-Za-z_][A-Za-z0-9_]*', line[pos:])
                if m:
                    word = m.group(0)
                    if word in RESERVED_WORDS:
                        all_tokens.append(("RESERVED_WORD", word, line_number))
                    elif word in DATA_TYPES:
                        all_tokens.append(("DATA_TYPE", word, line_number))
                    else:
                        all_tokens.append(("IDENTIFIER", word, line_number))
                    pos += len(word)
                    matched = True

            if not matched:
                raise TokenizeError(f"Line {line_number}: unexpected character '{line[pos]}'")

    return all_tokens


def print_token_report(tokens):
    """Prints a nicely formatted token table and summary."""
    print("BiteBit Token List")
    print("-" * 50)
    print("{:<18} {:<20} {}".format("Token Type", "Lexeme", "Line"))
    print("-" * 50)
    for token_type, lexeme, line_number in tokens:
        print("{:<18} {:<20} {}".format(token_type, lexeme, line_number))

    print()
    print("BiteBit Token Summary")
    print("-" * 30)
    types_seen = {}
    for t, lexeme, _ in tokens:
        types_seen.setdefault(t, []).append(lexeme)
    for t, lexemes in types_seen.items():
        print(f"  {t}: {len(lexemes)}")
