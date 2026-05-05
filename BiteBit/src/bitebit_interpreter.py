# -----------------------------------------------------------------------------------------------------
# BiteBit Language - Interpreter
# CMPSC 470 | Final Project
#
# The interpreter walks the AST produced by the parser and executes each statement.
# It uses the SymbolTable for storing and looking up variable values.
# -----------------------------------------------------------------------------------------------------

from bitebit_symbol_table import SymbolTable, SymbolTableError, get_type_name


class RuntimeError_(Exception):
    """Raised when a BiteBit program hits a runtime error."""
    pass


class Interpreter:
    def __init__(self):
        self.symbol_table = SymbolTable()

    def run(self, ast):
        """Execute all statements in the AST. Returns True if successful."""
        for stmt in ast:
            self.execute(stmt)

    def execute(self, stmt):
        """Execute a single AST statement node."""
        kind = stmt["kind"]

        if kind == "declaration":
            self.exec_declaration(stmt)
        elif kind == "assignment":
            self.exec_assignment(stmt)
        elif kind == "print":
            self.exec_print(stmt)
        else:
            raise RuntimeError_(f"Line {stmt.get('line', '?')}: unknown statement kind '{kind}'")

    def exec_declaration(self, stmt):
        """Handle: let x : Type = expr;"""
        name = stmt["name"]
        declared_type = stmt["type"]
        line = stmt["line"]

        value = self.eval_expr(stmt["expr"], line)
        actual_type = get_type_name(value)

        if actual_type != declared_type:
            raise RuntimeError_(
                f"Line {line}: type mismatch — '{name}' declared as {declared_type} "
                f"but got {actual_type}."
            )

        try:
            self.symbol_table.insert(name, declared_type, value)
        except SymbolTableError as e:
            raise RuntimeError_(f"Line {line}: {e}")

    def exec_assignment(self, stmt):
        """Handle: x = expr;"""
        name = stmt["name"]
        line = stmt["line"]

        value = self.eval_expr(stmt["expr"], line)

        try:
            self.symbol_table.update(name, value)
        except SymbolTableError as e:
            raise RuntimeError_(f"Line {line}: {e}")

    def exec_print(self, stmt):
        """Handle: print expr;"""
        line = stmt["line"]
        value = self.eval_expr(stmt["expr"], line)
        print(self.format_output(value))

    def eval_expr(self, node, line):
        """Evaluate an expression AST node and return its Python value."""
        kind = node["kind"]

        if kind == "literal":
            return node["value"]

        if kind == "identifier":
            name = node["name"]
            try:
                return self.symbol_table.get_value(name)
            except SymbolTableError as e:
                raise RuntimeError_(f"Line {line}: {e}")

        if kind == "binop":
            left = self.eval_expr(node["left"], line)
            right = self.eval_expr(node["right"], line)
            return self.apply_binop(node["op"], left, right, line)

        if kind == "unary":
            operand = self.eval_expr(node["operand"], line)
            return self.apply_unary(node["op"], operand, line)

        raise RuntimeError_(f"Line {line}: unknown expression kind '{kind}'")

    def apply_binop(self, op, left, right, line):
        """Apply a binary operator and return the result."""
        try:
            if op == "+":
                return left + right
            if op == "-":
                return left - right
            if op == "*":
                return left * right
            if op == "/":
                if right == 0:
                    raise RuntimeError_(f"Line {line}: division by zero.")
                return left // right  # integer division
            if op == "%":
                if right == 0:
                    raise RuntimeError_(f"Line {line}: modulo by zero.")
                return left % right
            if op == "&":
                return left & right
            if op == "|":
                return left | right
            if op == "^":
                return left ^ right
            if op == "<<":
                return left << right
            if op == ">>":
                return left >> right
            if op == "==":
                return left == right
            if op == "!=":
                return left != right
            if op == "<":
                return left < right
            if op == ">":
                return left > right
            if op == "<=":
                return left <= right
            if op == ">=":
                return left >= right
        except TypeError as e:
            raise RuntimeError_(f"Line {line}: operator '{op}' cannot be applied to these types — {e}")

        raise RuntimeError_(f"Line {line}: unknown operator '{op}'")

    def apply_unary(self, op, operand, line):
        """Apply a unary operator and return the result."""
        if op == "~":
            if not isinstance(operand, int):
                raise RuntimeError_(f"Line {line}: '~' can only be applied to Int values.")
            return ~operand
        raise RuntimeError_(f"Line {line}: unknown unary operator '{op}'")

    def format_output(self, value):
        """Format a value for print output."""
        if value is True:
            return "true"
        if value is False:
            return "false"
        if value is None:
            return "null"
        return str(value)
