# -----------------------------------------------------------------------------------------------------
# BiteBit Language - Parser
# CMPSC 470 | Final Project
#
# The parser takes a token list and builds an Abstract Syntax Tree (AST).
# The AST is a list of statement nodes (dicts).
#
# Supported statements in v1:
#   - Variable declaration:  let x : Int = <expr>;
#   - Assignment:            x = <expr>;
#   - Print statement:       print <expr>;
#
# Supported expressions:
#   - Int literals, Bool literals, String literals
#   - Binary literals (0b...) and Hex literals (0x...)
#   - Identifiers
#   - Binary operations: +  -  *  /  %  &  |  ^  <<  >>
#   - Comparison: ==  !=  <  >  <=  >=
#   - Unary negation: ~
# -----------------------------------------------------------------------------------------------------


class ParseError(Exception):
    """Raised when the parser encounters unexpected syntax."""
    pass


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    # --- Token navigation helpers ---

    def peek(self):
        """Return the current token without consuming it, or None at end."""
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def consume(self):
        """Return the current token and advance position."""
        token = self.tokens[self.pos]
        self.pos += 1
        return token

    def expect(self, token_type, lexeme=None):
        """
        Consume the next token and verify it matches the expected type (and optional lexeme).
        Raises ParseError if it does not match.
        """
        tok = self.peek()
        if tok is None:
            raise ParseError(f"Unexpected end of input, expected {token_type}")
        if tok[0] != token_type:
            raise ParseError(f"Line {tok[2]}: expected {token_type} but got {tok[0]} '{tok[1]}'")
        if lexeme is not None and tok[1] != lexeme:
            raise ParseError(f"Line {tok[2]}: expected '{lexeme}' but got '{tok[1]}'")
        return self.consume()

    def expect_symbol(self, sym):
        return self.expect("SYMBOL", sym)

    def expect_operator(self, op):
        return self.expect("OPERATOR", op)

    # --- Top-level parse ---

    def parse(self):
        """Parse all statements in the token stream and return an AST (list of nodes)."""
        statements = []
        while self.peek() is not None:
            stmt = self.parse_statement()
            if stmt is not None:
                statements.append(stmt)
        return statements

    def parse_statement(self):
        """Parse a single statement."""
        tok = self.peek()
        if tok is None:
            return None

        tok_type, lexeme, line = tok

        # Declaration: let x : Type = expr;
        if tok_type == "RESERVED_WORD" and lexeme == "let":
            return self.parse_declaration()

        # Print statement: print expr;
        if tok_type == "RESERVED_WORD" and lexeme == "print":
            return self.parse_print()

        # Assignment: x = expr;
        if tok_type == "IDENTIFIER":
            return self.parse_assignment()

        raise ParseError(f"Line {line}: unexpected token '{lexeme}'")

    def parse_declaration(self):
        """Parse: let name : Type = expr;"""
        self.expect("RESERVED_WORD", "let")
        name_tok = self.expect("IDENTIFIER")
        name = name_tok[1]
        line = name_tok[2]
        self.expect_symbol(":")
        type_tok = self.expect("DATA_TYPE")
        declared_type = type_tok[1]
        self.expect_operator("=")
        expr = self.parse_expression()
        self.expect_symbol(";")
        return {"kind": "declaration", "name": name, "type": declared_type, "expr": expr, "line": line}

    def parse_print(self):
        """Parse: print expr;"""
        print_tok = self.consume()  # consume 'print'
        line = print_tok[2]
        expr = self.parse_expression()
        self.expect_symbol(";")
        return {"kind": "print", "expr": expr, "line": line}

    def parse_assignment(self):
        """Parse: name = expr;"""
        name_tok = self.expect("IDENTIFIER")
        name = name_tok[1]
        line = name_tok[2]
        self.expect_operator("=")
        expr = self.parse_expression()
        self.expect_symbol(";")
        return {"kind": "assignment", "name": name, "expr": expr, "line": line}

    # --- Expression parsing (handles operator precedence) ---
    # Precedence (low to high):
    #   comparison: == != < > <= >=
    #   bitwise OR: |
    #   bitwise XOR: ^
    #   bitwise AND: &
    #   bit shifts: << >>
    #   additive: + -
    #   multiplicative: * / %
    #   unary: ~
    #   primary: literal, identifier, (expr)

    def parse_expression(self):
        return self.parse_comparison()

    def parse_comparison(self):
        left = self.parse_bitor()
        tok = self.peek()
        while tok and tok[0] == "OPERATOR" and tok[1] in ("==", "!=", "<", ">", "<=", ">="):
            op = self.consume()[1]
            right = self.parse_bitor()
            left = {"kind": "binop", "op": op, "left": left, "right": right}
            tok = self.peek()
        return left

    def parse_bitor(self):
        left = self.parse_bitxor()
        tok = self.peek()
        while tok and tok[0] == "OPERATOR" and tok[1] == "|":
            op = self.consume()[1]
            right = self.parse_bitxor()
            left = {"kind": "binop", "op": op, "left": left, "right": right}
            tok = self.peek()
        return left

    def parse_bitxor(self):
        left = self.parse_bitand()
        tok = self.peek()
        while tok and tok[0] == "OPERATOR" and tok[1] == "^":
            op = self.consume()[1]
            right = self.parse_bitand()
            left = {"kind": "binop", "op": op, "left": left, "right": right}
            tok = self.peek()
        return left

    def parse_bitand(self):
        left = self.parse_shift()
        tok = self.peek()
        while tok and tok[0] == "OPERATOR" and tok[1] == "&":
            op = self.consume()[1]
            right = self.parse_shift()
            left = {"kind": "binop", "op": op, "left": left, "right": right}
            tok = self.peek()
        return left

    def parse_shift(self):
        left = self.parse_additive()
        tok = self.peek()
        while tok and tok[0] == "OPERATOR" and tok[1] in ("<<", ">>"):
            op = self.consume()[1]
            right = self.parse_additive()
            left = {"kind": "binop", "op": op, "left": left, "right": right}
            tok = self.peek()
        return left

    def parse_additive(self):
        left = self.parse_multiplicative()
        tok = self.peek()
        while tok and tok[0] == "OPERATOR" and tok[1] in ("+", "-"):
            op = self.consume()[1]
            right = self.parse_multiplicative()
            left = {"kind": "binop", "op": op, "left": left, "right": right}
            tok = self.peek()
        return left

    def parse_multiplicative(self):
        left = self.parse_unary()
        tok = self.peek()
        while tok and tok[0] == "OPERATOR" and tok[1] in ("*", "/", "%"):
            op = self.consume()[1]
            right = self.parse_unary()
            left = {"kind": "binop", "op": op, "left": left, "right": right}
            tok = self.peek()
        return left

    def parse_unary(self):
        tok = self.peek()
        if tok and tok[0] == "OPERATOR" and tok[1] == "~":
            op = self.consume()[1]
            operand = self.parse_primary()
            return {"kind": "unary", "op": op, "operand": operand}
        return self.parse_primary()

    def parse_primary(self):
        tok = self.peek()
        if tok is None:
            raise ParseError("Unexpected end of input in expression")

        tok_type, lexeme, line = tok

        # Integer literal
        if tok_type == "INT_LITERAL":
            self.consume()
            return {"kind": "literal", "value": int(lexeme), "vtype": "Int"}

        # Binary literal like 0b1010
        if tok_type == "BINARY_LITERAL":
            self.consume()
            return {"kind": "literal", "value": int(lexeme, 2), "vtype": "Int"}

        # Hex literal like 0xF
        if tok_type == "HEX_LITERAL":
            self.consume()
            return {"kind": "literal", "value": int(lexeme, 16), "vtype": "Int"}

        # String literal
        if tok_type == "STRING":
            self.consume()
            # Strip surrounding quotes
            inner = lexeme[1:-1]
            return {"kind": "literal", "value": inner, "vtype": "String"}

        # Boolean literals
        if tok_type == "RESERVED_WORD" and lexeme == "true":
            self.consume()
            return {"kind": "literal", "value": True, "vtype": "Bool"}

        if tok_type == "RESERVED_WORD" and lexeme == "false":
            self.consume()
            return {"kind": "literal", "value": False, "vtype": "Bool"}

        # Identifier (variable reference)
        if tok_type == "IDENTIFIER":
            self.consume()
            return {"kind": "identifier", "name": lexeme}

        # Grouped expression: ( expr )
        if tok_type == "SYMBOL" and lexeme == "(":
            self.consume()
            expr = self.parse_expression()
            self.expect_symbol(")")
            return expr

        raise ParseError(f"Line {line}: unexpected token '{lexeme}' in expression")


def parse(tokens):
    """Convenience function: parse a token list and return an AST."""
    parser = Parser(tokens)
    return parser.parse()
