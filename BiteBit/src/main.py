# -----------------------------------------------------------------------------------------------------
# BiteBit Language - Main Entry Point
# CMPSC 470 | Final Project
#
# Usage: python src/main.py <file.bb>
#
# This script ties together all the BiteBit components:
#   1. Tokenizer   - Breaks source into tokens
#   2. Parser      - Builds an AST from tokens
#   3. Interpreter - Executes the AST
# -----------------------------------------------------------------------------------------------------

import sys
import os

# Make sure the src/ folder is on the path when running from project root
sys.path.insert(0, os.path.dirname(__file__))

from bitebit_tokenizer import tokenize, TokenizeError
from bitebit_parser import parse, ParseError
from bitebit_interpreter import Interpreter, RuntimeError_


def run_file(file_path):
    """Read and execute a BiteBit source file."""
    # Read the source file
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            source = f.read()
    except FileNotFoundError:
        print(f"Error: file '{file_path}' not found.")
        sys.exit(1)

    # Step 1: Tokenize
    try:
        tokens = tokenize(source)
    except TokenizeError as e:
        print(f"Tokenize Error: {e}")
        sys.exit(1)

    # Step 2: Parse
    try:
        ast = parse(tokens)
    except ParseError as e:
        print(f"Parse Error: {e}")
        sys.exit(1)

    # Step 3: Interpret
    interpreter = Interpreter()
    try:
        interpreter.run(ast)
    except RuntimeError_ as e:
        print(f"Runtime Error: {e}")
        sys.exit(1)


def main():
    if len(sys.argv) < 2:
        print("BiteBit Interpreter v1")
        print("Usage: python src/main.py <file.bb>")
        print("Example: python src/main.py examples/valid_basic.bb")
        sys.exit(0)

    file_path = sys.argv[1]
    run_file(file_path)


if __name__ == "__main__":
    main()
