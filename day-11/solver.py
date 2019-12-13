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

# Shared Code for this day
import io
import sys

def reset_stream(*args):
    for arg in args:
        arg.truncate(0)
        arg.seek(0)

def get_new_coords(current_coords, current_heading, new_direction):
    heading_map = {
        0: lambda x, y: (x, y + 1),
        1: lambda x, y: (x + 1, y),
        2: lambda x, y: (x, y - 1),
        3: lambda x, y: (x - 1, y),
    }
    direction_map = {
        0: lambda: 3 if current_heading - 1 < 0 else current_heading - 1,
        1: lambda: 0 if current_heading + 1 > 3 else current_heading + 1,
    }

    x, y = current_coords
    new_heading = direction_map[new_direction]()
    new_coords = heading_map[new_heading](x, y)
    return new_coords, new_heading

old_stdin = sys.stdin
old_stdout = sys.stdout

new_stdin = io.StringIO()
new_stdout = io.StringIO()

def paint(initial_panels):
    sys.stdin = new_stdin
    sys.stdout = new_stdout

    panels_painted = initial_panels
    current_coords = (0, 0)
    current_heading = 0
    loc = 0
    new_data = data.copy()

    while 1:
        reset_stream(new_stdin, new_stdout)
        if current_coords in panels_painted:
            current_panel_color = panels_painted[current_coords]
        else:
            current_panel_color = 0
        new_stdin.write(f'{current_panel_color}\n')
        new_stdin.seek(0)
        new_data, loc, return_code = operate(new_data, loc)
        new_panel_color, new_direction, _ = [int(x) if x else x for x in new_stdout.getvalue().split('\n')]
        panels_painted[current_coords] = new_panel_color
        current_coords, current_heading = get_new_coords(current_coords, current_heading, new_direction)
        if not return_code:
            break

    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return panels_painted

# Part 1
panels_painted = paint({})
print('Number of panels painted is', len(panels_painted))

# Part 2
panels_painted = paint({(0, 0): 1})
min_x = min(panels_painted, key=lambda x: x[0])[0]
min_y = min(panels_painted, key=lambda x: x[1])[1]
max_x = max(panels_painted, key=lambda x: x[0])[0]
max_y = max(panels_painted, key=lambda x: x[1])[1]

character_to_print = {
    0: ' ',
    1: '█'
}
for y in range(max_y, min_y - 1, -1):
    for x in range(min_x, max_x + 1):
        print(character_to_print[panels_painted.get((x, y), 0)], end='')
    print()
