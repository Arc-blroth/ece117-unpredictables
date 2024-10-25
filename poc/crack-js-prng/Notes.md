# RNG stuff

How to go from XORshift128+ (which produces 64-bit unsigned int) to a double (decimal)? 
- Create mantissa (Chrome/V8)
    - 64-bit UINT treated as mantissa: AND with 0xFFFFFFFFFFFFF ((1<<52)-1) (52-bit mantissa)
    - OR with 0x3FF0000000000000 to get a value between 1 and 2
    - Subtract 1 to get a value between 0 and 1

Retrieve part of the unsigned integer. To do this, take the Math.random() outputs and
- Add 1
- AND with 0xFFFFFFFFFFFFF ((1<<52)-1) to extract lower 52 bits of generated number