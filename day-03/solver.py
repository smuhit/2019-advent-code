
wire_paths = open('input').read().split()
wire_1 = wire_paths[0].split(',')
wire_2 = wire_paths[1].split(',')

def get_all_coords_of_wire(path):
	# Originally coords was a set
	# Modified to OrderedDict for Part 2 (including the addition of counter)
	current_pos = [0, 0]
	direction_map = {
		'R': (0, 1),
		'L': (0, -1),
		'U': (1, 1),
		'D': (1, -1)
	}
	coords = {}
	counter = 0
	for heading in path:
		direction = heading[0]
		magnitude = int(heading[1:])
		idx, step = direction_map[direction]
		for _ in range(magnitude):
			current_pos[idx] += step
			counter += 1
			coords[tuple(current_pos)] = counter
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