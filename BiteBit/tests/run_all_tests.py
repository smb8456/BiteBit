# -----------------------------------------------------------------------------------------------------
# BiteBit
# CMPSC 470 | Spring Semester
# Test Suite Runner
# -----------------------------------------------------------------------------------------------------

import subprocess
import sys
from pathlib import Path

tokenizer_program = Path("src/bitebit_tokenizer.py")
symbol_table_program = Path("src/bitebit_symbol_table.py")

tokenizer_folder = Path("tests/tokenizer")
symbol_table_folder = Path("tests/symbol_table")


def run_test(program_file, test_file):
    result = subprocess.run(
        [sys.executable, str(program_file), str(test_file)],
        capture_output=True,
        text=True
    )
    return result.stdout.strip()


def run_suite(title, program_file, test_folder):
    print("\n" + "=" * 50)
    print(title)
    print("=" * 50)

    passed = 0
    failed = 0

    test_files = sorted(test_folder.glob("*.txt"))

    for test_file in test_files:
        if test_file.name.endswith("_expected.txt"):
            continue

        expected_file = test_folder / "expected" / (test_file.stem + "_expected.txt")

        print("\nRunning:", test_file.name)

        try:
            actual_output = run_test(program_file, test_file)
        except Exception as error:
            print("FAIL")
            print("Could not run test:", error)
            failed += 1
            continue

        if expected_file.exists():
            expected_output = expected_file.read_text(encoding="utf-8").strip()

            if actual_output == expected_output:
                print("PASS")
                passed += 1
            else:
                print("FAIL")
                print("Expected:")
                print(expected_output)
                print("\nActual:")
                print(actual_output)
                failed += 1
        else:
            print("No expected file found for this test.")

    return passed, failed


def main():
    total_passed = 0
    total_failed = 0

    p1, f1 = run_suite("Tokenizer Tests", tokenizer_program, tokenizer_folder)
    total_passed += p1
    total_failed += f1

    p2, f2 = run_suite("Symbol Table Tests", symbol_table_program, symbol_table_folder)
    total_passed += p2
    total_failed += f2

    print("\n" + "=" * 50)
    print("Final Results")
    print("=" * 50)
    print("Passed:", total_passed)
    print("Failed:", total_failed)


if __name__ == "__main__":
    main()
