# -----------------------------------------------------------------------------------------------------
# BiteBit - Test Runner
# CMPSC 470 | Final Project
# Runs all BiteBit test suites and reports a combined summary.
# -----------------------------------------------------------------------------------------------------

import sys
import os
import subprocess

# Make sure we run from the project root
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(project_root)

test_files = [
    "tests/test_tokenizer.py",
    "tests/test_symbol_table.py",
    "tests/test_parser.py",
    "tests/test_interpreter.py",
]

print("=" * 55)
print("  BiteBit v1 - Full Test Suite")
print("=" * 55)
print()

overall_failed = 0

for test_file in test_files:
    print(f"Running {test_file}...")
    print("-" * 40)
    result = subprocess.run(
        [sys.executable, test_file],
        capture_output=False
    )
    if result.returncode != 0:
        overall_failed += 1
    print()

print("=" * 55)
if overall_failed == 0:
    print("  All test suites passed!")
else:
    print(f"  {overall_failed} test suite(s) had failures.")
print("=" * 55)

sys.exit(overall_failed)
