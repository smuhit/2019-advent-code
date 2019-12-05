data = [int(datum) for datum in open('input').read().split(',')]

operands = {
    1: (3, True, False, lambda x, y: x + y),
    2: (3, True, False, lambda x, y: x * y),
    3: (1, True, False, lambda : int(input('Enter a value:'))),
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

def operate(dataset):
    loc = 0
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
    return dataset

# Part 1 and 2
new_data = data.copy()
new_data = operate(new_data)  # with an input of 1 for part 1 and 5 for part 2
