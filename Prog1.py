# Prog1: Predictive Parser for the grammar
import sys

tokens = []
current_token = 0

def error():
    print("Rejected")
    sys.exit()

def match(expected):
    global current_token
    if current_token < len(tokens) and tokens[current_token] == expected:
        current_token += 1
    else:
        error()

def S():
    F()
    match('=')
    E()

def E():
    T()
    E_()

def E_():
    if current_token < len(tokens) and tokens[current_token] in ['+', '-']:
        op = tokens[current_token]
        match(op)
        T()
        E_()

def T():
    F()
    T_()

def T_():
    if current_token < len(tokens) and tokens[current_token] in ['*', '/']:
        op = tokens[current_token]
        match(op)
        F()
        T_()

def F():
    if current_token < len(tokens):
        if tokens[current_token] in ['a', 'b']:
            match(tokens[current_token])
        elif tokens[current_token] == '(':
            match('(')
            E()
            match(')')
        else:
            error()
    else:
        error()

def parse(input_string):
    global tokens, current_token
    tokens = [ch for ch in input_string if ch != ' ']  # Tokenize
    if tokens[-1] != '$':
        print("Input must end with $")
        return
    tokens = tokens[:-1]  # Remove $
    current_token = 0
    try:
        S()
        if current_token == len(tokens):
            print("Accepted")
        else:
            print("Rejected")
    except SystemExit:
        pass

# Test cases
inputs = [
    "a=(a+a)*b$",
    "(a)=a*(b-a)$",
    "a=(a+a)b$"
]

for line in inputs:
    print(f"Input: {line}")
    parse(line)
