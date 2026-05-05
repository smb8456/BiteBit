# -----------------------------------------------------------------------------------------------------
# BiteBit Language - Symbol Table and Type Checker
# CMPSC 470 | Final Project
#
# The SymbolTable class stores variable names, their declared types, and current values.
# It also enforces type rules when variables are updated.
# -----------------------------------------------------------------------------------------------------


def format_value(value):
    """Convert a Python value to a BiteBit-style string for display."""
    if value is True:
        return "true"
    if value is False:
        return "false"
    if value is None:
        return "null"
    if isinstance(value, str):
        return '"' + value + '"'
    return str(value)


def get_type_name(value):
    """Map a Python value to its BiteBit type name."""
    if isinstance(value, bool):
        return "Bool"
    if isinstance(value, int):
        return "Int"
    if isinstance(value, str):
        return "String"
    if value is None:
        return "Null"
    return "Unknown"


class SymbolTableError(Exception):
    """Raised for type errors or undeclared variable access."""
    pass


class SymbolTable:
    """
    Stores variable entries.
    Each entry has a 'type' (string like 'Int', 'Bool', 'String') and a 'value'.
    """

    def __init__(self):
        self.table = {}

    def insert(self, name, data_type, value):
        """Declare a new variable. Raises SymbolTableError if already declared."""
        if name in self.table:
            raise SymbolTableError(f"Duplicate declaration: '{name}' was already declared.")
        self.table[name] = {"type": data_type, "value": value}

    def lookup(self, name):
        """Return the entry dict for a variable, or None if not found."""
        return self.table.get(name)

    def get_value(self, name):
        """Return the current value of a variable. Raises error if not declared."""
        entry = self.table.get(name)
        if entry is None:
            raise SymbolTableError(f"Undeclared variable: '{name}' was not declared.")
        return entry["value"]

    def update(self, name, value):
        """Update a variable's value. Raises SymbolTableError on type mismatch."""
        if name not in self.table:
            raise SymbolTableError(f"Undeclared variable: '{name}' was not declared.")
        expected_type = self.table[name]["type"]
        actual_type = get_type_name(value)
        if expected_type != actual_type:
            raise SymbolTableError(
                f"Type mismatch: '{name}' is type {expected_type} but got {actual_type}."
            )
        self.table[name]["value"] = value

    def print_table(self):
        """Print the current symbol table contents."""
        print("Symbol Table")
        print("-" * 45)
        print("{:<15} {:<10} {}".format("Name", "Type", "Value"))
        print("-" * 45)
        for name, info in self.table.items():
            print("{:<15} {:<10} {}".format(name, info["type"], format_value(info["value"])))
        print("-" * 45)
