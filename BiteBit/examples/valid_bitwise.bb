// valid_bitwise.bb
// Demonstrates bitwise and arithmetic operations in BiteBit.

let a : Int = 0b11001100;   // 204 in decimal
let b : Int = 0b10101010;   // 170 in decimal

let and_result : Int = a & b;
print and_result;

let or_result : Int = a | b;
print or_result;

let xor_result : Int = a ^ b;
print xor_result;

let shift_left : Int = 1 << 4;
print shift_left;

let shift_right : Int = 256 >> 3;
print shift_right;

let hex_val : Int = 0xFF;
let masked : Int = hex_val & 0x0F;
print masked;
