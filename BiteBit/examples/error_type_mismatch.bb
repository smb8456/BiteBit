// error_type_mismatch.bb
// This program should produce a type error.
// 'count' is declared as Int but we try to assign a String.

let count : Int = "oops";
print count;
