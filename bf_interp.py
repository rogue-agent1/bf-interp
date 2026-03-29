#!/usr/bin/env python3
"""bf_interp: Brainfuck interpreter."""
import sys

def interpret(code, input_data="", tape_size=30000, max_steps=1000000):
    # Strip non-BF chars
    code = "".join(c for c in code if c in "+-<>.,[]")
    tape = [0] * tape_size
    ptr = 0
    ip = 0
    input_pos = 0
    output = []
    steps = 0
    # Precompute bracket pairs
    brackets = {}
    stack = []
    for i, c in enumerate(code):
        if c == "[": stack.append(i)
        elif c == "]":
            if not stack: raise SyntaxError("Unmatched ]")
            j = stack.pop()
            brackets[j] = i
            brackets[i] = j
    if stack: raise SyntaxError("Unmatched [")
    while ip < len(code) and steps < max_steps:
        c = code[ip]
        if c == "+": tape[ptr] = (tape[ptr] + 1) % 256
        elif c == "-": tape[ptr] = (tape[ptr] - 1) % 256
        elif c == ">": ptr = (ptr + 1) % tape_size
        elif c == "<": ptr = (ptr - 1) % tape_size
        elif c == ".": output.append(chr(tape[ptr]))
        elif c == ",":
            tape[ptr] = ord(input_data[input_pos]) if input_pos < len(input_data) else 0
            input_pos += 1
        elif c == "[":
            if tape[ptr] == 0: ip = brackets[ip]
        elif c == "]":
            if tape[ptr] != 0: ip = brackets[ip]
        ip += 1
        steps += 1
    return "".join(output)

def test():
    # Hello World
    hello = "++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++."
    assert interpret(hello) == "Hello World!\n"
    # Cat (echo input)
    assert interpret(",[.,]", "abc") == "abc"
    # Add two numbers (3+5)
    add = ",>++++++++++++++++++++++++++++++++++++++++++++++++.,."
    # Simple: increment and print
    result = interpret("++++++++++++++++++++++++++++++++++++++++++++++++.")  # 48 = '0'
    assert result == "0"
    # Loop counter
    result2 = interpret("+++[>+<-]>.")  # tape[1] = 3, print chr(3)
    assert result2 == chr(3)
    # Syntax error
    try:
        interpret("[")
        assert False
    except SyntaxError:
        pass
    print("All tests passed!")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test": test()
    elif len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            print(interpret(f.read()))
    else: print("Usage: bf_interp.py <file.bf> | bf_interp.py test")
