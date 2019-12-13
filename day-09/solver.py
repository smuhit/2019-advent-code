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
    3: (1, True,  False, lambda : int(input('Enter Input: '))),
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

# Part 1 and 2 (value 1 for part 1 and 2 for part 2)
operate(data)