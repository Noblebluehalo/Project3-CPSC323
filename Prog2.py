# Prog2: LR parser based on given LR parsing table

# Grammar rules:
# 1: E -> E + T
# 2: E -> E - T
# 3: E -> T
# 4: T  ->T * F
# 5: T -> T / F
# 6: T -> F
# 7: F -> ( E )
# 8: F -> i

# Each production
productions = {
    1: ('E', 3),
    2: ('E', 3),
    3: ('E', 1),
    4: ('T', 3),
    5: ('T', 3),
    6: ('T', 1),
    7: ('F', 3),
    8: ('F', 1)
}

# ACTION table: (state, terminal) -> action
# e.g., 'S5' = shift to state 5, 'R3' = reduce by rule 3, 'acc' = accept
action_table = {
    0: {'i': 'S5', '(': 'S4'},
    1: {'+': 'S6', '-': 'S7', '$': 'acc'},
    2: {'+': 'R3', '-': 'R3', '*': 'S8', '/': 'S9', ')': 'R3', '$': 'R3'},
    3: {'+': 'R6', '-': 'R6', '*': 'R6', '/': 'R6', ')': 'R6', '$': 'R6'},
    4: {'i': 'S5', '(': 'S4'},
    5: {'+': 'R8', '-': 'R8', '*': 'R8', '/': 'R8', ')': 'R8', '$': 'R8'},
    6: {'i': 'S5', '(': 'S4'},
    7: {'i': 'S5', '(': 'S4'},
    8: {'i': 'S5', '(': 'S4'},
    9: {'i': 'S5', '(': 'S4'},
    10: {'+': 'S6', '-': 'S7', ')': 'S15'},
    11: {'+': 'R1', '-': 'R1', '*': 'S8', '/': 'S9', ')': 'R1', '$': 'R1'},
    12: {'+': 'R2', '-': 'R2', '*': 'S8', '/': 'S9', ')': 'R2', '$': 'R2'},
    13: {'+': 'R4', '-': 'R4', '*': 'R4', '/': 'R4', ')': 'R4', '$': 'R4'},
    14: {'+': 'R5', '-': 'R5', '*': 'R5', '/': 'R5', ')': 'R5', '$': 'R5'},
    15: {'+': 'R7', '-': 'R7', '*': 'R7', '/': 'R7', ')': 'R7', '$': 'R7'}
}

# GOTO table: (state, nonterminal) -> next state
goto_table = {
    0: {'E': 1, 'T': 2, 'F': 3},
    4: {'E': 10, 'T': 2, 'F': 3},
    6: {'T': 11, 'F': 3},
    7: {'T': 12, 'F': 3},
    8: {'F': 13},
    9: {'F': 14}
}

def lr_parse(input_string):
    stack = [0]
    tokens = [ch for ch in input_string if ch != ' ']

    index = 0
    print(f"\nParsing: {input_string}")
    print("Stack\t\tInput\t\tAction")

    while True:
        state = stack[-1]
        current_token = tokens[index] if index < len(tokens) else '$'
        action = action_table.get(state, {}).get(current_token, '')

        # Print current step
        stack_str = ' '.join(map(str, stack))
        input_str = ''.join(tokens[index:])
        print(f"{stack_str:<16}{input_str:<16}{action}")

        if action == '':
            print("Rejected")
            return

        if action == 'acc':
            print("Accepted")
            return

        if action.startswith('S'):
            # Shift
            next_state = int(action[1:])
            stack.append(current_token)
            stack.append(next_state)
            index += 1
        elif action.startswith('R'):
            # Reduce
            prod_num = int(action[1:])
            lhs, rhs_len = productions[prod_num]

            for _ in range(2 * rhs_len):
                stack.pop()
            current_state = stack[-1]
            stack.append(lhs)
            next_state = goto_table[current_state][lhs]
            stack.append(next_state)

# Test cases
test_inputs = [
    "(i+i)*i$",
    "(i*)$"
]

for test in test_inputs:
    lr_parse(test)


