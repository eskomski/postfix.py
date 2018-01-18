'''
Elliott Skomski (skomski.org)
postfix.py: a PostFix interpreter
'''

import argparse

def check_stack_len(n):
    if len(stack) < n:
        print('err: fewer than %d items on stack')
        exit(1)

def add_cmd():
    check_stack_len(2)
    v1 = stack.pop()
    v2 = stack.pop()

    stack.append(v1 + v2)

def sub_cmd():
    check_stack_len(2)
    v1 = stack.pop()
    v2 = stack.pop()

    stack.append(v2 - v1)

def mul_cmd():
    check_stack_len(2)
    v1 = stack.pop()
    v2 = stack.pop()

    stack.append(v2 * v1)

def div_cmd():
    check_stack_len(2)
    v1 = stack.pop()
    v2 = stack.pop()

    stack.append(v2 // v1)

def rem_cmd():
    check_stack_len(2)
    v1 = stack.pop()
    v2 = stack.pop()

    stack.append(v2 % v1)

def pop_cmd():
    check_stack_len(1)
    stack.pop()

def eq_cmd():
    check_stack_len(2)
    v1 = stack.pop()
    v2 = stack.pop()

    stack.append(int(v2 == v1))

def lt_cmd():
    check_stack_len(2)
    v1 = stack.pop()
    v2 = stack.pop()

    stack.append(int(v2 < v1))

def gt_cmd():
    check_stack_len(2)
    v1 = stack.pop()
    v2 = stack.pop()

    stack.append(int(v2 > v1))

def sel_cmd():
    check_stack_len(3)
    v1 = stack.pop()
    v2 = stack.pop()
    v3 = stack.pop()

    if v3 == 0:
        stack.append(v1)
    else:
        stack.append(v2)

def nget_cmd():
    check_stack_len(1)
    v_index = stack.pop()
    check_stack_len(v_index)
    stack.append(stack[-v_index])

def swap_cmd():
    check_stack_len(2)

    v1 = stack.pop()
    v2 = stack.pop()

    stack.append(v1)
    stack.append(v2)

cmd = {'add' : add_cmd,
       'sub' : sub_cmd,
       'mul' : mul_cmd,
       'div' : div_cmd,
       'rem' : rem_cmd,
       'pop' : pop_cmd,
       'eq'  : eq_cmd,
       'lt'  : lt_cmd,
       'gt'  : gt_cmd,
       'sel' : sel_cmd,
       'nget': nget_cmd,
       'swap': swap_cmd}

def match_parens(n, start=1):
    parens = 1
    for i in range(start, len(n)):
        if n[i] == '(':
            parens += 1
        elif n[i] == ')':
            parens -= 1
            if parens == 0:
                break
    if parens != 0:
        raise SyntaxError
    return i

def tokenize(n):
    done = False
    tokens = []
    while not done:
        if n.startswith('('):
            i = match_parens(n)
            tokens.append(n[:i+1])
            n = n[i+1:].strip()
            continue
        split = n.split(maxsplit=1)
        tokens.append(split[0])
        if len(split) < 2:
            done = True
        else:
            n = split[1]
    return tokens

def is_int(n):
    try:
        n = int(n)
    except ValueError:
        return False

    return True

parser = argparse.ArgumentParser()
parser.add_argument('prog', type=str)
parser.add_argument('-args', nargs='+', type=int)
parser.add_argument('-v', action='store_true')
args = parser.parse_args()

prog = args.prog

if not prog.startswith('(postfix'):
    print('err: prefix not found')
    exit()

prog = prog.split(maxsplit=1)[1]
prog = prog[:-1]

tokens = tokenize(prog)

nargs = int(tokens[0])
if (nargs != 0 and (args.args == None or len(args.args) != nargs)) or (nargs == 0 and args.args != None):
    print('err: mismatched number of arguments')
    exit(2)

stack = []
for a in args.args:
    stack.insert(0, a)

tokens = tokens[1:]

while len(tokens) != 0:
    tok = tokens[0]
    tokens = tokens[1:]
    if is_int(tok):
        stack.append(int(tok))
    elif tok.startswith('('):
        stack.append(tok)
    elif tok == 'exec':
        seq = stack.pop()
        if not seq.startswith('(') or not seq.endswith(')'):
            print('err: no executable sequence at TOS')
            exit(4)
        seq = tokenize(seq.strip('(').strip(')'))
        seq.reverse()
        for t in seq:
            tokens.insert(0, t)
    else:
        cmd[tok]()
    if (args.v):
        print('stack:', stack)

print(stack[-1])

