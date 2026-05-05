# -----------------------------------------------------------------------------------------------------
# BiteBit - Interpreter Tests
# -----------------------------------------------------------------------------------------------------

import sys
import os
import io
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from bitebit_tokenizer import tokenize
from bitebit_parser import parse
from bitebit_interpreter import Interpreter, RuntimeError_


def run_program(source):
    """Run a BiteBit source string and return stdout as a string."""
    tokens = tokenize(source)
    ast = parse(tokens)
    interp = Interpreter()
    captured = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = captured
    try:
        interp.run(ast)
    finally:
        sys.stdout = old_stdout
    return captured.getvalue().strip()


def test_print_int():
    out = run_program("let x : Int = 42;\nprint x;")
    assert out == "42", f"Expected '42', got '{out}'"
    print("PASS test_print_int")


def test_print_string():
    out = run_program('let s : String = "hello";\nprint s;')
    assert out == "hello", f"Expected 'hello', got '{out}'"
    print("PASS test_print_string")


def test_print_bool_true():
    out = run_program("let b : Bool = true;\nprint b;")
    assert out == "true"
    print("PASS test_print_bool_true")


def test_print_bool_false():
    out = run_program("let b : Bool = false;\nprint b;")
    assert out == "false"
    print("PASS test_print_bool_false")


def test_arithmetic_add():
    out = run_program("let r : Int = 3 + 4;\nprint r;")
    assert out == "7"
    print("PASS test_arithmetic_add")


def test_arithmetic_subtract():
    out = run_program("let r : Int = 10 - 3;\nprint r;")
    assert out == "7"
    print("PASS test_arithmetic_subtract")


def test_arithmetic_multiply():
    out = run_program("let r : Int = 6 * 7;\nprint r;")
    assert out == "42"
    print("PASS test_arithmetic_multiply")


def test_integer_division():
    out = run_program("let r : Int = 10 / 3;\nprint r;")
    assert out == "3"  # integer division
    print("PASS test_integer_division")


def test_modulo():
    out = run_program("let r : Int = 10 % 3;\nprint r;")
    assert out == "1"
    print("PASS test_modulo")


def test_binary_literal():
    out = run_program("let x : Int = 0b1010;\nprint x;")
    assert out == "10"
    print("PASS test_binary_literal")


def test_hex_literal():
    out = run_program("let x : Int = 0xF;\nprint x;")
    assert out == "15"
    print("PASS test_hex_literal")


def test_bitwise_and():
    out = run_program("let r : Int = 0b1111 & 0b1010;\nprint r;")
    assert out == "10"
    print("PASS test_bitwise_and")


def test_bitwise_or():
    out = run_program("let r : Int = 0b1100 | 0b0011;\nprint r;")
    assert out == "15"
    print("PASS test_bitwise_or")


def test_bitwise_xor():
    out = run_program("let r : Int = 0b1111 ^ 0b1010;\nprint r;")
    assert out == "5"
    print("PASS test_bitwise_xor")


def test_shift_left():
    out = run_program("let r : Int = 1 << 4;\nprint r;")
    assert out == "16"
    print("PASS test_shift_left")


def test_shift_right():
    out = run_program("let r : Int = 256 >> 3;\nprint r;")
    assert out == "32"
    print("PASS test_shift_right")


def test_bitwise_not():
    out = run_program("let r : Int = ~0;\nprint r;")
    assert out == "-1"
    print("PASS test_bitwise_not")


def test_comparison_equal():
    out = run_program("let r : Bool = 5 == 5;\nprint r;")
    assert out == "true"
    print("PASS test_comparison_equal")


def test_comparison_not_equal():
    out = run_program("let r : Bool = 5 != 3;\nprint r;")
    assert out == "true"
    print("PASS test_comparison_not_equal")


def test_reassignment():
    out = run_program("let x : Int = 1;\nx = 99;\nprint x;")
    assert out == "99"
    print("PASS test_reassignment")


def test_type_mismatch_raises():
    try:
        run_program('let x : Int = "hello";')
        print("FAIL test_type_mismatch_raises: expected RuntimeError_")
    except RuntimeError_:
        print("PASS test_type_mismatch_raises")


def test_duplicate_decl_raises():
    try:
        run_program("let x : Int = 1;\nlet x : Int = 2;")
        print("FAIL test_duplicate_decl_raises: expected RuntimeError_")
    except RuntimeError_:
        print("PASS test_duplicate_decl_raises")


def test_undeclared_var_raises():
    try:
        run_program("print z;")
        print("FAIL test_undeclared_var_raises: expected RuntimeError_")
    except RuntimeError_:
        print("PASS test_undeclared_var_raises")


def test_variable_reference_in_expr():
    out = run_program("let x : Int = 5;\nlet y : Int = x + 3;\nprint y;")
    assert out == "8"
    print("PASS test_variable_reference_in_expr")


if __name__ == "__main__":
    tests = [
        test_print_int,
        test_print_string,
        test_print_bool_true,
        test_print_bool_false,
        test_arithmetic_add,
        test_arithmetic_subtract,
        test_arithmetic_multiply,
        test_integer_division,
        test_modulo,
        test_binary_literal,
        test_hex_literal,
        test_bitwise_and,
        test_bitwise_or,
        test_bitwise_xor,
        test_shift_left,
        test_shift_right,
        test_bitwise_not,
        test_comparison_equal,
        test_comparison_not_equal,
        test_reassignment,
        test_type_mismatch_raises,
        test_duplicate_decl_raises,
        test_undeclared_var_raises,
        test_variable_reference_in_expr,
    ]

    passed = 0
    failed = 0
    for t in tests:
        try:
            t()
            passed += 1
        except Exception as e:
            print(f"FAIL {t.__name__}: {e}")
            failed += 1

    print(f"\nInterpreter: {passed} passed, {failed} failed")
    if failed:
        sys.exit(1)
