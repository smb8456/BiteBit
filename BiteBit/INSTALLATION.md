# BiteBit - Installation and Setup

## Requirements

- Python 3.8 or higher
- No external libraries needed (BiteBit uses only the Python standard library)

## Installation

1. Download or unzip the BiteBit project folder.

2. Open a terminal and navigate into the project folder:

```bash
cd BiteBit
```

3. That's it. No install step is needed. BiteBit uses only built-in Python modules.

---

## Running a BiteBit Program

```bash
python src/main.py examples/valid_basic.bb
```

You can run any `.bb` file the same way:

```bash
python src/main.py examples/valid_bitwise.bb
python src/main.py examples/valid_strings_bool.bb
```

---

## Running the Tests

```bash
python tests/run_all_tests.py
```

This will run all four test suites (tokenizer, parser, symbol table, interpreter) and print a summary.

---

## Checking for Errors

The error example files show what BiteBit error messages look like:

```bash
python src/main.py examples/error_type_mismatch.bb
python src/main.py examples/error_duplicate_decl.bb
python src/main.py examples/error_undeclared_var.bb
```

---

## Troubleshooting

- If you see `ModuleNotFoundError`, make sure you are running from inside the `BiteBit/` project folder.
- BiteBit source files use the `.bb` extension, but the interpreter can read any text file.
