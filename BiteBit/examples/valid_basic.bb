// valid_basic.bb
// Basic BiteBit v1 example covering Int, String, Bool, binary, and hex literals.

let x : Int = 0b1010;
let y : Int = 5;
let total : Int = x + y;
print total;

let mask : Int = 0xF;
let result : Int = total & mask;
print result;

let name : String = "BiteBit";
print name;

let active : Bool = true;
print active;
