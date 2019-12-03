data = [int(datum) for datum in open('input').read().split(',')]

operands = {1: lambda x, y: x + y, 2: lambda x, y: x * y}

def operate(dataset):
    loc = 0
    while loc <= len(dataset) and dataset[loc] != 99:
        dataset[dataset[loc + 3]] = operands[dataset[loc]](dataset[dataset[loc + 1]], dataset[dataset[loc + 2]])
        loc += 4
    return dataset

# Part 1
new_data = data.copy()
new_data[1] = 12
new_data[2] = 2
new_data = operate(new_data)
print("After program halts, the value at position 0 is", new_data[0])


# Part 2
result_to_find = 19690720
found = False
for noun in range(100):
    for verb in range(100):
        new_data = data.copy()
        new_data[1] = noun
        new_data[2] = verb
        new_data = operate(new_data)
        if new_data[0] == result_to_find:
            print("Found, Noun:", noun, "Verb:", verb)
            found = True
            break
    if found:
        break
