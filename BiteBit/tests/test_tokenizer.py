# -----------------------------------------------------------------------------------------------------
# BiteBit - Tokenizer Tests
# -----------------------------------------------------------------------------------------------------

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from bitebit_tokenizer import tokenize, TokenizeError


def test_basic_declaration():
    tokens = tokenize('let x : Int = 5;')
    types = [t[0] for t in tokens]
    lexemes = [t[1] for t in tokens]
    assert "RESERVED_WORD" in types
    assert "IDENTIFIER" in types
    assert "DATA_TYPE" in types
    assert "INT_LITERAL" in types
    assert "let" in lexemes
    assert "x" in lexemes
    assert "Int" in lexemes
    assert "5" in lexemes
    print("PASS test_basic_declaration")


def test_binary_literal():
    tokens = tokenize('let a : Int = 0b1010;')
    types = [t[0] for t in tokens]
    assert "BINARY_LITERAL" in types
    bin_tok = [t for t in tokens if t[0] == "BINARY_LITERAL"]
    assert bin_tok[0][1] == "0b1010"
    print("PASS test_binary_literal")


def test_hex_literal():
    tokens = tokenize('let h : Int = 0xFF;')
    types = [t[0] for t in tokens]
    assert "HEX_LITERAL" in types
    hex_tok = [t for t in tokens if t[0] == "HEX_LITERAL"]
    assert hex_tok[0][1] == "0xFF"
    print("PASS test_hex_literal")


def test_string_literal():
    tokens = tokenize('let s : String = "hello";')
    string_toks = [t for t in tokens if t[0] == "STRING"]
    assert len(string_toks) == 1
    assert string_toks[0][1] == '"hello"'
    print("PASS test_string_literal")


def test_bool_literals():
    tokens = tokenize('let b : Bool = true;')
    reserved = [t for t in tokens if t[0] == "RESERVED_WORD"]
    lexemes = [t[1] for t in reserved]
    assert "true" in lexemes
    print("PASS test_bool_literals")


def test_operators():
    tokens = tokenize('let r : Int = 3 + 4 * 2;')
    ops = [t[1] for t in tokens if t[0] == "OPERATOR"]
    assert "+" in ops
    assert "*" in ops
    print("PASS test_operators")


def test_bitwise_operators():
    tokens = tokenize('let r : Int = a & b | c ^ d;')
    ops = [t[1] for t in tokens if t[0] == "OPERATOR"]
    assert "&" in ops
    assert "|" in ops
    assert "^" in ops
    print("PASS test_bitwise_operators")


def test_shift_operators():
    tokens = tokenize('let r : Int = 1 << 3;')
    ops = [t[1] for t in tokens if t[0] == "OPERATOR"]
    assert "<<" in ops
    print("PASS test_shift_operators")


def test_comments_skipped():
    tokens = tokenize('// this is a comment\nlet x : Int = 1;')
    lexemes = [t[1] for t in tokens]
    assert "this" not in lexemes
    assert "comment" not in lexemes
    assert "x" in lexemes
    print("PASS test_comments_skipped")


def test_inline_comment_stripped():
    tokens = tokenize('let x : Int = 5; // inline comment')
    lexemes = [t[1] for t in tokens]
    assert "inline" not in lexemes
    assert "x" in lexemes
    print("PASS test_inline_comment_stripped")


def test_print_keyword():
    tokens = tokenize('print x;')
    reserved = [t for t in tokens if t[0] == "RESERVED_WORD"]
    assert any(t[1] == "print" for t in reserved)
    print("PASS test_print_keyword")


def test_line_numbers():
    source = "let x : Int = 1;\nlet y : Int = 2;"
    tokens = tokenize(source)
    line_nums = set(t[2] for t in tokens)
    assert 1 in line_nums
    assert 2 in line_nums
    print("PASS test_line_numbers")


if __name__ == "__main__":
    tests = [
        test_basic_declaration,
        test_binary_literal,
        test_hex_literal,
        test_string_literal,
        test_bool_literals,
        test_operators,
        test_bitwise_operators,
        test_shift_operators,
        test_comments_skipped,
        test_inline_comment_stripped,
        test_print_keyword,
        test_line_numbers,
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

    print(f"\nTokenizer: {passed} passed, {failed} failed")
    if failed:
        sys.exit(1)
