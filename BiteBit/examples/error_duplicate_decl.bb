// error_duplicate_decl.bb
// This program should produce a duplicate declaration error.

let x : Int = 5;
let x : Int = 10;   // Error: x was already declared
print x;
