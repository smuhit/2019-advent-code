data = {k: v for v, k in [x.split(')') for x in open('input').read().split()]}

# PART 1

total_orbit = 0
for node in data:
	node_orbit = 0
	new_node = node
	while new_node in data:
		node_orbit += 1
		new_node = data[new_node]
	total_orbit += node_orbit

print('Total number of direct and indirect orbits is', total_orbit)


# PART 2

source = 'YOU'
dest = 'SAN'

routes = {source: [], dest: []}

for route in routes:
	node = route
	while node in data:
		node = data[node]
		routes[route].append(node)

common = None
for node in routes[source]:
	if node in routes[dest]:
		common = node
		break

print('Shortest hop between YOU and SAN is',routes[source].index(common) + routes[dest].index(common))