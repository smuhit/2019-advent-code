import functools
import math

raw_data = open('input').read().split('\n')

def get_original_position(raw_data):
    moon_positions = {}
    for idx, line in enumerate(raw_data):
        positions = []
        for loc in line[1:-1].split(', '):
            positions.append(int(loc.split('=')[-1]))
        moon_positions[idx] = positions
    moon_velocity = {k: [0, 0, 0] for k in range(len(moon_positions))}
    return moon_positions, moon_velocity

def apply_gravity(moon_positions, moon_velocity):
    for base_moon in range(0, len(moon_positions) - 1):
        for comp_moon in range(base_moon + 1, len(moon_positions)):
            for idx, val in enumerate(moon_positions[base_moon]):
                if val > moon_positions[comp_moon][idx]:
                    moon_velocity[comp_moon][idx] += 1
                    moon_velocity[base_moon][idx] -= 1
                elif val < moon_positions[comp_moon][idx]:
                    moon_velocity[comp_moon][idx] -= 1
                    moon_velocity[base_moon][idx] += 1

def apply_velocity(moon_positions, moon_velocity):
    for moon in moon_positions:
        for idx, _ in enumerate(moon_positions[moon]):
            moon_positions[moon][idx] += moon_velocity[moon][idx]

def calculate_total_energy(moon_positions, moon_velocity):
    energy = 0
    for moon in moon_positions:
        energy += sum([abs(x) for x in moon_positions[moon]]) * sum([abs(x) for x in moon_velocity[moon]])
    return energy

# Part 1

moon_positions, moon_velocity = get_original_position(raw_data)
steps = 1000

for _ in range(1000):
    apply_gravity(moon_positions, moon_velocity)
    apply_velocity(moon_positions, moon_velocity)

print(f'Total energy in moon system after {steps} steps is', calculate_total_energy(moon_positions, moon_velocity))

# Part 2

def get_current_position_velocities(moon_positions, moon_velocity):
    position_velocities = []
    for k in range(len(moon_positions[0])):
        position_velocity_axis_builder = []
        for moon in moon_positions:
            position_velocity_axis_builder.append(moon_positions[moon][k])
            position_velocity_axis_builder.append(moon_velocity[moon][k])
        position_velocities.append(tuple(position_velocity_axis_builder))
    return position_velocities

def lcm(*numbers):
    def singular_lcm(a, b):
        return a * b // math.gcd(a, b)
    return functools.reduce(singular_lcm, numbers)

moon_positions, moon_velocity = get_original_position(raw_data)
steps = 0
seen_positions_velocities = {k: set() for k in range(len(moon_positions[0]))}
done = [False] * len(moon_positions[0])

while any([not x for x in done]):
    current_position_velocities = get_current_position_velocities(moon_positions, moon_velocity)
    for idx, val in enumerate(current_position_velocities):
        if not(done[idx]):
            if val in seen_positions_velocities[idx]:
                done[idx] = steps
            else:
                seen_positions_velocities[idx].add(val)
    apply_gravity(moon_positions, moon_velocity)
    apply_velocity(moon_positions, moon_velocity)
    steps += 1

print('Number of steps until a position/velocity is revisited is', lcm(*done))