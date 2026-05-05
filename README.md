# BiteBit v1

BiteBit is a small explicitly typed programming language focused on binary, hexadecimal, and bitwise operations. The final BiteBit v1 implementation includes tokenization, parsing for a selected subset, symbol table management, type checking, and simple interpretation of BiteBit programs.

BiteBit was created as a final project for CMPSC 470.

---

## Quick Start

Run a BiteBit program:

```bash
python src/main.py examples/valid_basic.bb
```

Run all tests:

```bash
python tests/run_all_tests.py
```

---

## What BiteBit v1 Supports

- Typed variable declarations (`let x : Int = 5;`)
- Assignment statements (`x = 10;`)
- `print` statements
- Integer, binary (`0b...`), and hex (`0x...`) literals
- String and Bool literals
- Arithmetic operators: `+  -  *  /  %`
- Bitwise operators: `&  |  ^  ~  <<  >>`
- Comparison operators: `==  !=  <  >  <=  >=`
- Single-line comments (`//`)
- Type checking and helpful error messages

## Future Work (Not in v1)

- `if` / `else` conditionals
- `while` loops
- Functions (`fn`) and `return`
- Arrays and structs
- Full compiler / code generation backend

---

## Project Structure

```
BiteBit/
├── README.md
├── INSTALLATION.md
├── requirements.txt
├── .gitignore
├── src/
│   ├── main.py                   # Entry point
│   ├── bitebit_tokenizer.py      # Lexer
│   ├── bitebit_parser.py         # Parser / AST builder
│   ├── bitebit_symbol_table.py   # Symbol table and type checker
│   └── bitebit_interpreter.py    # Interpreter / runtime
├── examples/
│   ├── valid_basic.bb
│   ├── valid_bitwise.bb
│   ├── valid_strings_bool.bb
│   ├── error_type_mismatch.bb
│   ├── error_duplicate_decl.bb
│   └── error_undeclared_var.bb
├── tests/
│   ├── run_all_tests.py
│   ├── test_tokenizer.py
│   ├── test_parser.py
│   ├── test_symbol_table.py
│   └── test_interpreter.py
```
