# -----------------------------------------------------------------------------------------------------
# BiteBit
# CMPSC 470 | Spring Semester
# BiteBit Symbol Table
# -----------------------------------------------------------------------------------------------------

import re
import sys


#--> This class stores variables in a dictionary.
# Each variable name maps to its type and current value.
class SymbolTable:
    def __init__(self):
        self.table = {}

    def insert(self, name, data_type, value):
        if name in self.table:
            print("Error: duplicate declaration for", name)
            return

        self.table[name] = {"type": data_type, "value": value}

    def lookup(self, name):
        return self.table.get(name)

    def update(self, name, value):
        if name not in self.table:
            print("Error: variable", name, "was not declared")
            return

        expected_type = self.table[name]["type"]
        actual_type = get_type_name(value)

        if expected_type != actual_type:
            print("Error: type mismatch for", name)
            return

        self.table[name]["value"] = value

    def print_table(self, title):
        print("\n" + title)
        print("-" * 45)
        print("{:<12} {:<10} {:<15}".format("Name", "Type", "Value"))
        print("-" * 45)

        for name, info in self.table.items():
            print("{:<12} {:<10} {:<15}".format(name, info["type"], format_value(info["value"])))

        print("-" * 45)


#--> Convert Python values back into BiteBit-style output
def format_value(value):
    if value is True:
        return "true"
    if value is False:
        return "false"
    if value is None:
        return "null"
    if isinstance(value, str):
        return '"' + value + '"'
    return str(value)


#--> Figure out which BiteBit type a Python value matches
def get_type_name(value):
    if isinstance(value, bool):
        return "Bool"
    if isinstance(value, int):
        return "Int"
    if isinstance(value, str):
        return "String"
    if value is None:
        return "Null"
    return "Unknown"


#--> Replace BiteBit words and variables so Python can evaluate the expression
def evaluate_expression(expression, symbol_table):
    expr = expression.strip()

    # Save string literals first so variable replacement does not touch them
    saved_strings = []

    def save_string(match):
        saved_strings.append(match.group(0))
        return f"§{len(saved_strings) - 1}§"

    expr = re.sub(r'"[^"\\]*(?:\\.[^"\\]*)*"', save_string, expr)

    # Replace BiteBit literals with Python versions
    expr = re.sub(r'\btrue\b', 'True', expr)
    expr = re.sub(r'\bfalse\b', 'False', expr)
    expr = re.sub(r'\bnull\b', 'None', expr)

    # Replace BiteBit logical operators with Python ones
    expr = expr.replace("&&", " and ")
    expr = expr.replace("||", " or ")
    expr = re.sub(r'(?<![=!<>])!(?!=)', ' not ', expr)

    # Use integer division
    expr = expr.replace("/", "//")

    # Replace identifiers with their current values
    def replace_name(match):
        name = match.group(0)

        if name in {"True", "False", "None", "and", "or", "not"}:
            return name

        entry = symbol_table.lookup(name)
        if entry is None:
            raise NameError(name)

        value = entry["value"]
        return repr(value)

    expr = re.sub(r'\b[A-Za-z_][A-Za-z0-9_]*\b', replace_name, expr)

    # Put strings back
    for i, text in enumerate(saved_strings):
        expr = expr.replace(f"§{i}§", text)

    try:
        return eval(expr, {"__builtins__": None}, {})
    except ZeroDivisionError:
        print("Error: division by zero")
        return None
    except NameError as error:
        print("Error: variable", str(error), "was not declared")
        return None
    except Exception:
        print("Error: invalid expression ->", expression)
        return None


#--> Read BiteBit source from a file
if len(sys.argv) > 1:
    file_name = sys.argv[1]
else:
    file_name = input("Enter BiteBit file name: ").strip()

try:
    with open(file_name, "r", encoding="utf-8") as file:
        source_code = file.read()
except FileNotFoundError:
    print("Error: file not found.")
    sys.exit()


#--> Create the symbol table object
symbol_table = SymbolTable()

#--> Split the file into lines
lines = source_code.split("\n")

#--> Patterns for typed declarations and assignments
declaration_pattern = r'let\s+([A-Za-z_][A-Za-z0-9_]*)\s*:\s*(Int|String|Bool|Null)\s*=\s*(.+);'
assignment_pattern = r'([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.+);'


#--> Helper function so we can skip if/while/fn blocks in this preliminary version
def cleaned_lines(source_lines):
    result = []
    skip_depth = 0

    for line in source_lines:
        line = line.strip()

        if line == "":
            continue

        if line.startswith("//"):
            continue

        if "//" in line:
            line = line.split("//")[0].strip()

        if line == "":
            continue

        if skip_depth > 0:
            skip_depth += line.count("{")
            skip_depth -= line.count("}")
            continue

        if line.startswith("if") or line.startswith("while") or line.startswith("fn") or line.startswith("else"):
            skip_depth += line.count("{")
            skip_depth -= line.count("}")
            continue

        if line in ["{", "}"]:
            continue

        result.append(line)

    return result


usable_lines = cleaned_lines(lines)


#--> FIRST PASS: process declarations only
for line in usable_lines:
    if line.startswith("let"):
        match = re.fullmatch(declaration_pattern, line)

        if match:
            var_name = match.group(1)
            data_type = match.group(2)
            expression = match.group(3).strip()

            value = evaluate_expression(expression, symbol_table)

            if value is None and data_type != "Null":
                continue

            if get_type_name(value) == data_type:
                symbol_table.insert(var_name, data_type, value)
            else:
                print("Error: invalid value for", var_name)


#--> Print symbol table before updates
symbol_table.print_table("Symbol Table Before Updates")

#--> SECOND PASS: process assignments only
for line in usable_lines:
    if not line.startswith("let"):
        match = re.fullmatch(assignment_pattern, line)

        if match:
            var_name = match.group(1)
            expression = match.group(2).strip()

            value = evaluate_expression(expression, symbol_table)

            if value is None and expression != "null":
                continue

            symbol_table.update(var_name, value)


#--> Print symbol table after updates
symbol_table.print_table("Symbol Table After Updates")
