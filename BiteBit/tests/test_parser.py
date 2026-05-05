# -----------------------------------------------------------------------------------------------------
# BiteBit - Parser Tests
# -----------------------------------------------------------------------------------------------------

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from bitebit_tokenizer import tokenize
from bitebit_parser import parse, ParseError


def parse_source(source):
    return parse(tokenize(source))


def test_declaration_node():
    ast = parse_source("let x : Int = 5;")
    assert len(ast) == 1
    stmt = ast[0]
    assert stmt["kind"] == "declaration"
    assert stmt["name"] == "x"
    assert stmt["type"] == "Int"
    assert stmt["expr"]["kind"] == "literal"
    assert stmt["expr"]["value"] == 5
    print("PASS test_declaration_node")


def test_print_node():
    ast = parse_source("let x : Int = 3;\nprint x;")
    assert len(ast) == 2
    assert ast[1]["kind"] == "print"
    print("PASS test_print_node")


def test_assignment_node():
    ast = parse_source("let x : Int = 1;\nx = 10;")
    assert ast[1]["kind"] == "assignment"
    assert ast[1]["name"] == "x"
    print("PASS test_assignment_node")


def test_binary_expression():
    ast = parse_source("let r : Int = 3 + 4;")
    expr = ast[0]["expr"]
    assert expr["kind"] == "binop"
    assert expr["op"] == "+"
    assert expr["left"]["value"] == 3
    assert expr["right"]["value"] == 4
    print("PASS test_binary_expression")


def test_binary_literal_parsed():
    ast = parse_source("let x : Int = 0b1010;")
    expr = ast[0]["expr"]
    assert expr["kind"] == "literal"
    assert expr["value"] == 10  # 0b1010 = 10
    print("PASS test_binary_literal_parsed")


def test_hex_literal_parsed():
    ast = parse_source("let x : Int = 0xF;")
    expr = ast[0]["expr"]
    assert expr["value"] == 15  # 0xF = 15
    print("PASS test_hex_literal_parsed")


def test_bool_literal():
    ast = parse_source("let b : Bool = true;")
    expr = ast[0]["expr"]
    assert expr["value"] is True
    print("PASS test_bool_literal")


def test_string_literal():
    ast = parse_source('let s : String = "hello";')
    expr = ast[0]["expr"]
    assert expr["value"] == "hello"
    print("PASS test_string_literal")


def test_comparison_expression():
    ast = parse_source("let r : Bool = 5 == 5;")
    expr = ast[0]["expr"]
    assert expr["kind"] == "binop"
    assert expr["op"] == "=="
    print("PASS test_comparison_expression")


def test_unary_bitwise_not():
    ast = parse_source("let r : Int = ~5;")
    expr = ast[0]["expr"]
    assert expr["kind"] == "unary"
    assert expr["op"] == "~"
    print("PASS test_unary_bitwise_not")


def test_multiple_statements():
    src = "let x : Int = 1;\nlet y : Int = 2;\nprint x;"
    ast = parse_source(src)
    assert len(ast) == 3
    print("PASS test_multiple_statements")


def test_missing_semicolon_raises():
    try:
        parse_source("let x : Int = 5")
        print("FAIL test_missing_semicolon_raises: expected ParseError")
    except ParseError:
        print("PASS test_missing_semicolon_raises")


if __name__ == "__main__":
    tests = [
        test_declaration_node,
        test_print_node,
        test_assignment_node,
        test_binary_expression,
        test_binary_literal_parsed,
        test_hex_literal_parsed,
        test_bool_literal,
        test_string_literal,
        test_comparison_expression,
        test_unary_bitwise_not,
        test_multiple_statements,
        test_missing_semicolon_raises,
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

    print(f"\nParser: {passed} passed, {failed} failed")
    if failed:
        sys.exit(1)
