#!/usr/bin/env python3
"""bf_interp - Brainfuck interpreter with optimization."""
import sys

def bf_run(code, input_data="", tape_size=30000):
    tape = [0] * tape_size
    ptr = 0
    ip = 0
    inp_idx = 0
    output = []
    jumps = {}
    stack = []
    for i, c in enumerate(code):
        if c == "[": stack.append(i)
        elif c == "]":
            j = stack.pop()
            jumps[j] = i
            jumps[i] = j
    while ip < len(code):
        c = code[ip]
        if c == ">": ptr += 1
        elif c == "<": ptr -= 1
        elif c == "+": tape[ptr] = (tape[ptr] + 1) % 256
        elif c == "-": tape[ptr] = (tape[ptr] - 1) % 256
        elif c == ".": output.append(chr(tape[ptr]))
        elif c == ",":
            tape[ptr] = ord(input_data[inp_idx]) if inp_idx < len(input_data) else 0
            inp_idx += 1
        elif c == "[":
            if tape[ptr] == 0: ip = jumps[ip]
        elif c == "]":
            if tape[ptr] != 0: ip = jumps[ip]
        ip += 1
    return "".join(output)

def bf_optimize(code):
    optimized = []
    i = 0
    clean = "".join(c for c in code if c in "><+-.,[]")
    while i < len(clean):
        c = clean[i]
        if c in "><+-":
            count = 0
            while i < len(clean) and clean[i] == c:
                count += 1
                i += 1
            optimized.append((c, count))
        else:
            optimized.append((c, 1))
            i += 1
    return optimized

def test():
    hello = "++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++."
    result = bf_run(hello)
    assert result == "Hello World!\n"
    cat = ",.,.,."
    result2 = bf_run(cat, "ABC")
    assert result2 == "ABC"
    add = ",>,<[->+<]>."
    result3 = bf_run(add, "\x02\x03")
    assert ord(result3) == 5
    assert bf_run("") == ""
    clear = "[-]"
    assert bf_run("+++++" + clear + ".") == "\x00"
    opt = bf_optimize("+++>>>---<<<")
    assert ("+", 3) in opt
    assert (">", 3) in opt
    print("All tests passed!")

if __name__ == "__main__":
    test() if "--test" in sys.argv else print("bf_interp: Brainfuck interpreter. Use --test")
