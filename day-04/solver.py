import re

min_input = 158126
max_input = 624574

# Part 1
criteria = []
for x in range(min_input, max_input + 1):
	digits = [int(digit) for digit in str(x)]
	has_double = any(x == digits[idx + 1] for idx, x in enumerate(digits[:-1]))
	increasing = all(x >= digits[idx] for idx, x in enumerate(digits[1:]))
	if has_double and increasing:
		criteria.append(x)

print('Amount of numbers in range that meet the doubles and increasing criteria are', len(criteria))

# Part 2
num_criteria = 0
for x in criteria:
	digit_groups = [m.group(0) for m in re.finditer(r"(\d)\1*", str(x))]
	has_only_doubles = any(len(x) == 2 for x in digit_groups)
	if has_only_doubles:
		num_criteria += 1

print('Amount of numbers in range that meet the doubles (and no greater) and increasing criteria are', num_criteria)
