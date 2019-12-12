data = [int(datum) for datum in open('input').read().split(',')]

operands = {
    1: (3, True, False, lambda x, y: x + y),
    2: (3, True, False, lambda x, y: x * y),
    3: (1, True, False, lambda : int(input())),
    4: (1, False, False, lambda x: print(x)),
    5: (2, False, True, lambda x, y: y if x != 0 else None),
    6: (2, False, True, lambda x, y: y if x == 0 else None),
    7: (3, True, False, lambda x, y: 1 if x < y else 0),
    8: (3, True, False, lambda x, y: 1 if x == y else 0),
}

def get_value(dataset, location, mode):
    if mode == 1:
        return dataset[location]
    elif mode == 0:
        return dataset[dataset[location]]

def operate(dataset, loc=0):
    return_code = 0
    try:
        while loc < len(dataset) and dataset[loc] != 99:
            raw_value = dataset[loc]
            operand = raw_value % 100
            param_modes = [(raw_value // 100) % 10, (raw_value // 1000) % 10, (raw_value // 10000) % 10]
            offset, to_save, change_pointer, func = operands[operand]
            values = []
            for x in range(1, offset + int(not to_save)):
                param_mode = param_modes[x - 1]
                values.append(get_value(dataset, loc + x, param_mode))
            value = func(*values)
            if to_save:
                dataset[dataset[loc + offset]] = value
            if change_pointer and value is not None:
                loc = value
            else:
                loc += offset + 1
    except EOFError:
        return_code = 1
    return dataset, loc, return_code

# Part 1

import itertools
import io
import sys

old_stdin = sys.stdin
old_stdout = sys.stdout

new_stdin = io.StringIO()
new_stdout = io.StringIO()

sys.stdin = new_stdin
sys.stdout = new_stdout

max_value = None

phase_settings = list(itertools.permutations(range(5), 5))

for phase_setting in phase_settings:
    input_signal = 0
    for phase in phase_setting:
        new_stdin.write(f'{phase}\n{input_signal}\n')
        new_stdin.seek(0)
        new_data = data.copy()
        new_data = operate(new_data)
        new_stdin.truncate(0)
        new_stdin.seek(0)
        input_signal = int(new_stdout.getvalue().strip())
        new_stdout.truncate(0)
        new_stdout.seek(0)
    if max_value is None or input_signal > max_value:
        max_value = input_signal
sys.stdin = old_stdin
sys.stdout = old_stdout
print('Highest thruster signal is', max_value)

# Part 2
sys.stdin = new_stdin
sys.stdout = new_stdout

max_value = None

phase_settings = list(itertools.permutations(range(5, 10), 5))
for phase_setting in phase_settings:
    input_signal = 0
    idx = 0
    in_progress = [True] * 5
    data_stack = [None] * 5
    new_stdin.truncate(0)
    new_stdin.seek(0)
    new_stdout.truncate(0)
    new_stdout.seek(0)
    while any(in_progress):
        if in_progress[idx]:
            phase = phase_setting[idx]
            if not data_stack[idx]:
                new_stdin.write(f'{phase}\n{input_signal}\n')
                new_data = data.copy()
                loc = 0            
            else:
                new_stdin.write(f'{input_signal}\n')
                new_data, loc = data_stack[idx]
            new_stdin.seek(0)
            new_data, loc, return_code = operate(new_data, loc)
            if return_code == 1:
                data_to_push = (new_data.copy(), loc)
                data_stack[idx] = data_to_push
            elif return_code == 0 and idx == 4:
                final_value = int(new_stdout.getvalue().split('\n')[-2])
                in_progress[idx] = False
                break
            elif return_code == 0:
                in_progress[idx] = False
            new_stdin.truncate(0)
            new_stdin.seek(0)
            input_signal = new_stdout.getvalue().strip()
            new_stdout.truncate(0)
            new_stdout.seek(0)
        idx += 1
        if idx >= 5:
            idx = 0
    if max_value is None or final_value > max_value:
        max_value = final_value
sys.stdin = old_stdin
sys.stdout = old_stdout
print('Highest feedback loop thruster signal is', max_value)