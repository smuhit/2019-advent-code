from collections import defaultdict

raw_data = [int(datum) for datum in open('input').read().split(',')]

data = defaultdict(lambda: 0)
for idx, val in enumerate(raw_data):
    data[idx] = val

relative_base = 0

def adjust_relative(amount):
    global relative_base
    relative_base += amount

operands = {
    1: (3, True,  False, lambda x, y: x + y),
    2: (3, True,  False, lambda x, y: x * y),
    3: (1, True,  False, lambda : int(input())),
    4: (1, False, False, lambda x: print(x)),
    5: (2, False, True,  lambda x, y: y if x != 0 else None),
    6: (2, False, True,  lambda x, y: y if x == 0 else None),
    7: (3, True,  False, lambda x, y: 1 if x < y else 0),
    8: (3, True,  False, lambda x, y: 1 if x == y else 0),
    9: (1, False, False, adjust_relative)
}

def get_destination(dataset, location, mode):
    mode_map = {
        0: lambda: dataset[location],
        1: lambda: location,
        2: lambda: dataset[location] + relative_base,
    }
    return mode_map[mode]()

def get_value(dataset, location, mode):
    return dataset[get_destination(dataset, location, mode)]

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
                dataset[get_destination(dataset, loc + offset, param_modes[offset - 1])] = value
            if change_pointer and value is not None:
                loc = value
            else:
                loc += offset + 1
    except EOFError:
        return_code = 1
    return dataset, loc, return_code

# Part 1
import io
import sys

old_stdout = sys.stdout
new_stdout = io.StringIO()
sys.stdout = new_stdout

new_data = data.copy()
operate(new_data)
intcode_output = [int(x) for x in new_stdout.getvalue().strip().split('\n')]
num_block_tiles = len(list(filter(lambda x: x == 2, [intcode_output[x] for x in range(2, len(intcode_output), 3)])))

sys.stdout = old_stdout

print('Number of block tiles is', num_block_tiles)

# Part 2 --- Play a game of breakout to find the answer

def reset_stream(stream):
    stream.truncate(0)
    stream.seek(0)

reset_stream(new_stdout)
display = defaultdict(lambda: defaultdict(lambda: ' '))

def show_display_and_get_input():
    intcode_output = [int(x) for x in new_stdout.getvalue().strip().split('\n')]
    code_to_character = {
        0: ' ',
        1: '█',
        2: '\033[92m□\033[0m',
        3: '\033[90m▔\033[0m',
        4: '\033[94m●\033[0m'
    }
    for x in range(0, len(intcode_output), 3):
        if intcode_output[x + 2] in code_to_character:
            display[intcode_output[x + 1]][intcode_output[x]] = code_to_character[intcode_output[x + 2]]
        else:
            display[intcode_output[x + 1]][intcode_output[x]] = f'\033[1mSCORE: {intcode_output[x + 2]}\033[0m'
    sys.stdout = old_stdout
    print("\033c", end="")
    if 0 in display.keys() and -1 in display[0]:
        print(display[0][-1])
    for y in range(min(display.keys()), max(display.keys()) + 1):
        if y in display:
            line = ''
            for x in range(min(display[y].keys()), max(display[y].keys()) + 1):
                if x != -1 or y != 0:
                    if x in display[y]:
                        line += display[y][x]
            print(line)
    reset_stream(new_stdout)
    char_map = {  # because typing -1 is a bore...
        'a': -1,
        's': 0,
        'd': 1
    }
    entered_char = input('Which way should the joystick move? ').lower()
    while entered_char not in char_map:
        entered_char = input('Please enter a, s, or d. Which way should the joystick move? ').lower()
    val = char_map[entered_char]
    sys.stdout = new_stdout
    return val

operands[3] = (1, True,  False, show_display_and_get_input)
new_data = data.copy()
new_data[0] = 2

sys.stdout = new_stdout
operate(new_data)