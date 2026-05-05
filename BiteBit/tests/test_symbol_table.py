# -----------------------------------------------------------------------------------------------------
# BiteBit - Symbol Table Tests
# -----------------------------------------------------------------------------------------------------

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from bitebit_symbol_table import SymbolTable, SymbolTableError


def test_insert_and_lookup():
    st = SymbolTable()
    st.insert("x", "Int", 10)
    entry = st.lookup("x")
    assert entry is not None
    assert entry["type"] == "Int"
    assert entry["value"] == 10
    print("PASS test_insert_and_lookup")


def test_duplicate_declaration_raises():
    st = SymbolTable()
    st.insert("x", "Int", 5)
    try:
        st.insert("x", "Int", 10)
        print("FAIL test_duplicate_declaration_raises: expected SymbolTableError")
    except SymbolTableError:
        print("PASS test_duplicate_declaration_raises")


def test_update_value():
    st = SymbolTable()
    st.insert("x", "Int", 5)
    st.update("x", 99)
    assert st.lookup("x")["value"] == 99
    print("PASS test_update_value")


def test_type_mismatch_on_update():
    st = SymbolTable()
    st.insert("x", "Int", 5)
    try:
        st.update("x", "hello")
        print("FAIL test_type_mismatch_on_update: expected SymbolTableError")
    except SymbolTableError:
        print("PASS test_type_mismatch_on_update")


def test_undeclared_update_raises():
    st = SymbolTable()
    try:
        st.update("z", 10)
        print("FAIL test_undeclared_update_raises: expected SymbolTableError")
    except SymbolTableError:
        print("PASS test_undeclared_update_raises")


def test_get_value():
    st = SymbolTable()
    st.insert("flag", "Bool", True)
    val = st.get_value("flag")
    assert val is True
    print("PASS test_get_value")


def test_get_value_undeclared_raises():
    st = SymbolTable()
    try:
        st.get_value("y")
        print("FAIL test_get_value_undeclared_raises: expected SymbolTableError")
    except SymbolTableError:
        print("PASS test_get_value_undeclared_raises")


def test_string_type():
    st = SymbolTable()
    st.insert("msg", "String", "hello")
    entry = st.lookup("msg")
    assert entry["type"] == "String"
    assert entry["value"] == "hello"
    print("PASS test_string_type")


def test_bool_type():
    st = SymbolTable()
    st.insert("b", "Bool", False)
    st.update("b", True)
    assert st.lookup("b")["value"] is True
    print("PASS test_bool_type")


if __name__ == "__main__":
    tests = [
        test_insert_and_lookup,
        test_duplicate_declaration_raises,
        test_update_value,
        test_type_mismatch_on_update,
        test_undeclared_update_raises,
        test_get_value,
        test_get_value_undeclared_raises,
        test_string_type,
        test_bool_type,
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

    print(f"\nSymbol Table: {passed} passed, {failed} failed")
    if failed:
        sys.exit(1)
