import math
import operator

asteroids = set()

raw_data = open('input').read().split()

for y_idx, line in enumerate(raw_data):
    for x_idx, char in enumerate(line):
        if char == '#':
            asteroids.add((x_idx, y_idx))

# Part 1 (and viewable_asteroids for part 2)
max_viewable = None
for asteroid in asteroids:
    viewable_asteroids = set()
    num_viewable = 0
    for potential_visible_asteroid in asteroids - {asteroid}:
        x_distance = abs(asteroid[0] - potential_visible_asteroid[0])
        y_distance = abs(asteroid[1] - potential_visible_asteroid[1])
        factor = math.gcd(x_distance, y_distance)
        x_factor = x_distance // factor
        y_factor = y_distance // factor
        x_direction = x_factor if asteroid[0] < potential_visible_asteroid[0] else -x_factor
        y_direction = y_factor if asteroid[1] < potential_visible_asteroid[1] else -y_factor
        x_coord = asteroid[0] + x_direction
        y_coord = asteroid[1] + y_direction
        viewable = True
        while (x_coord, y_coord) != potential_visible_asteroid:
            if (x_coord, y_coord) in asteroids:
                viewable = False
                break
            x_coord += x_direction
            y_coord += y_direction
        if viewable:
            num_viewable += 1
            viewable_asteroids.add(potential_visible_asteroid)
    if not max_viewable or num_viewable > max_viewable[0]:
        max_viewable = num_viewable, asteroid, viewable_asteroids

print('Maximum number of asteroids viewable is', max_viewable[0])

# Part 2

_, asteroid, viewable_asteroids = max_viewable
quads = {
    1: [],
    2: [],
    3: [],
    4: [],
}

for viewable_asteroid in viewable_asteroids:
    if viewable_asteroid[0] >= asteroid[0] and viewable_asteroid[1] < asteroid[1]:
        quadrant = 1
        slope = (viewable_asteroid[0] - asteroid[0]) / (asteroid[1] - viewable_asteroid[1])
    elif viewable_asteroid[0] > asteroid[0] and viewable_asteroid[1] >= asteroid[1]:
        quadrant = 2
        slope = (viewable_asteroid[1] - asteroid[1]) / (viewable_asteroid[0] - asteroid[0])
    elif viewable_asteroid[0] <= asteroid[0] and viewable_asteroid[1] > asteroid[1]:
        quadrant = 3
        slope = (viewable_asteroid[0] - asteroid[0]) / (viewable_asteroid[1] - asteroid[1])
    else:
        quadrant = 4
        slope = (asteroid[1] - viewable_asteroid[1]) / (asteroid[0] - viewable_asteroid[0])
    distance = abs(asteroid[0] - viewable_asteroid[0]) + abs(asteroid[1] - viewable_asteroid[1])
    quads[quadrant].append((slope, distance, viewable_asteroid))
for quad in quads:
    quads[quad].sort(key=operator.itemgetter(0, 1))
elem_200 = (quads[1] + quads[2] + quads[3] + quads[4])[199][2]
print('200th asteroid to die is', elem_200)