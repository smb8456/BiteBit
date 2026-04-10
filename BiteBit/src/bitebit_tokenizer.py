# -----------------------------------------------------------------------------------------------------
# BiteBit
# CMPSC 470 | Spring Semester
# BiteBit Tokenizer
# -----------------------------------------------------------------------------------------------------

import re
import sys

#--> Basic BiteBit definitions
reserved_words = {"let", "fn", "return", "if", "else", "while", "true", "false", "null"}
data_types = {"Int", "Bool", "String", "Null"}
operators = ["==", "!=", "<=", ">=", "<<", ">>", "&&", "||", "+", "-", "*", "/", "%", "=", "<", ">", "!", "&", "|", "^", "~"]
symbols = [":", ";", ",", "(", ")", "{", "}"]


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


#--> Lists to store tokens and report info
all_tokens = []
literals_found = []
operators_found = []
variables_found = []
reserved_found = []
data_types_found = []
symbols_found = []
duplicate_variables = []

declared_variables = set()
line_count = 0

lines = source_code.split("\n")

for line_number, line in enumerate(lines, start=1):
    line = line.strip()

    if line == "":
        continue

    # Skip full line comments
    if line.startswith("//"):
        continue

    # Remove inline comments
    if "//" in line:
        line = line.split("//")[0].strip()

    if line == "":
        continue

    line_count += 1

    # Find string literals first
    string_literals = re.findall(r'"[^"\\]*(?:\\.[^"\\]*)*"', line)
    for item in string_literals:
        literals_found.append(item)
        all_tokens.append(("STRING", item, line_number))
        line = line.replace(item, " ")

    # Find hex literals
    hex_literals = re.findall(r'\b0x[0-9A-Fa-f]+\b', line)
    for item in hex_literals:
        literals_found.append(item)
        all_tokens.append(("HEX_LITERAL", item, line_number))
        line = re.sub(r'\b' + re.escape(item) + r'\b', ' ', line)

    # Find binary literals
    binary_literals = re.findall(r'\b0b[01]+\b', line)
    for item in binary_literals:
        literals_found.append(item)
        all_tokens.append(("BINARY_LITERAL", item, line_number))
        line = re.sub(r'\b' + re.escape(item) + r'\b', ' ', line)

    # Find decimal literals
    decimal_literals = re.findall(r'\b\d+\b', line)
    for item in decimal_literals:
        literals_found.append(item)
        all_tokens.append(("INT_LITERAL", item, line_number))
        line = re.sub(r'\b' + re.escape(item) + r'\b', ' ', line)

    # Find operators (longer ones first)
    temp_line = line
    for op in operators:
        while op in temp_line:
            operators_found.append(op)
            all_tokens.append(("OPERATOR", op, line_number))
            temp_line = temp_line.replace(op, " ", 1)
    line = temp_line

    # Find symbols
    temp_line = line
    for sym in symbols:
        while sym in temp_line:
            symbols_found.append(sym)
            all_tokens.append(("SYMBOL", sym, line_number))
            temp_line = temp_line.replace(sym, " ", 1)
    line = temp_line

    # Find identifiers, keywords, and types
    words = re.findall(r'\b[A-Za-z_][A-Za-z0-9_]*\b', line)
    expecting_variable = False

    for word in words:
        if word in reserved_words:
            reserved_found.append(word)
            all_tokens.append(("RESERVED_WORD", word, line_number))

            if word == "let":
                expecting_variable = True

            if word in {"true", "false", "null"}:
                literals_found.append(word)

        elif word in data_types:
            data_types_found.append(word)
            all_tokens.append(("DATA_TYPE", word, line_number))

        else:
            variables_found.append(word)
            all_tokens.append(("IDENTIFIER", word, line_number))

            if expecting_variable:
                if word in declared_variables:
                    duplicate_variables.append(word)
                else:
                    declared_variables.add(word)
                expecting_variable = False


#--> Remove duplicates for final report lists
literal_list = sorted(set(literals_found))
operator_list = sorted(set(operators_found))
variable_list = sorted(set(variables_found))
reserved_list = sorted(set(reserved_found))
data_type_list = sorted(set(data_types_found))
symbol_list = sorted(set(symbols_found))
duplicate_list = sorted(set(duplicate_variables))


#--> Print token list
print("BiteBit Token List")
print("-" * 45)
print("{:<15} {:<15} {}".format("Token Type", "Lexeme", "Line"))
print("-" * 45)
for token_type, lexeme, line_number in all_tokens:
    print("{:<15} {:<15} {}".format(token_type, lexeme, line_number))

print()
print("BiteBit Token Report")
print("-" * 30)
print("Lines processed:", line_count)
print()

print("Number of literals:", len(literal_list))
print("Literals:", literal_list)
print()

print("Number of operators:", len(operator_list))
print("Operators:", operator_list)
print()

print("Number of identifiers:", len(variable_list))
print("Identifiers:", variable_list)
print()

print("Duplicate variable declarations:", duplicate_list)
print()

print("Number of reserved words:", len(reserved_list))
print("Reserved words:", reserved_list)
print()

print("Number of data types:", len(data_type_list))
print("Data types:", data_type_list)
print()

print("Number of symbols:", len(symbol_list))
print("Symbols:", symbol_list)
