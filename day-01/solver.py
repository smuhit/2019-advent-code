
data = open('input').read().split()

# PART 1
fuel = 0
for datum in data:
    fuel += int(datum) // 3 - 2

print('Fuel needed is', fuel)


# Part 2
fuel = 0
for datum in data:
    fuel_needed = int(datum) // 3 - 2
    fuel += fuel_needed
    while fuel_needed > 5:
        fuel_needed = int(fuel_needed) // 3 - 2
        fuel += fuel_needed

print('Actual Fuel needed is', fuel)