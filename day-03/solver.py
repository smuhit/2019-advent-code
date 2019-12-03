from collections import OrderedDict

wire_paths = open('input').read().split()
wire_1 = wire_paths[0].split(',')
wire_2 = wire_paths[1].split(',')

def get_all_coords_of_wire(path):
	# Originally coords was a set
	# Modified to OrderedDict for Part 2 (including the addition of counter)
	current_x = 0
	current_y = 0
	coords = OrderedDict()
	counter = 0
	for heading in path:
		direction = heading[0]
		magnitude = int(heading[1:])
		# Gah... Hate massive if-else, but easiest solution
		if direction == 'R':
			for new_x in range(current_x + 1, current_x + magnitude + 1):
				counter += 1
				coords[(new_x, current_y)] = counter
			current_x = new_x
		elif direction == 'L':
			for new_x in range(current_x - 1, current_x - magnitude - 1, -1):
				counter += 1
				coords[(new_x, current_y)] = counter
			current_x = new_x
		elif direction == 'U':
			for new_y in range(current_y + 1, current_y + magnitude + 1):
				counter += 1
				coords[(current_x, new_y)] = counter
			current_y = new_y
		elif direction == 'D':
			for new_y in range(current_y - 1, current_y - magnitude - 1, -1):
				counter += 1
				coords[(current_x, new_y)] = counter
			current_y = new_y
	return coords

# Part 1
wire_1_coords = get_all_coords_of_wire(wire_1)
wire_2_coords = get_all_coords_of_wire(wire_2)

min_distance = None
for intersect in wire_1_coords.keys() & wire_2_coords.keys():
	if not min_distance or abs(intersect[0]) + abs(intersect[1]) < min_distance:
		min_distance = abs(intersect[0]) + abs(intersect[1])

print('Minimum Manhattan distance of wires crossing from start is', min_distance)

# Part 2
min_steps = None
for intersect in wire_1_coords.keys() & wire_2_coords.keys():
	if not min_steps or wire_1_coords[intersect] + wire_2_coords[intersect] < min_steps:
		min_steps = wire_1_coords[intersect] + wire_2_coords[intersect]

print('Minimum number of steps of wires getting to intersection is', min_steps)