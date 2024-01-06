from collections import deque

#
# Process input
#
with open('day 18/input.txt') as file:
    cubes = set(map(lambda x: tuple(map(int, x.split(','))), file.read().splitlines()))

#
# Puzzle 1
#
surface_area = 0
for x, y, z in cubes:
    neighbors = {(x+1, y, z), (x-1, y, z), (x, y+1, z), (x, y-1, z), (x, y, z+1), (x, y, z-1)}
    surface_area += 6 - len(neighbors & cubes)

print(f'Puzzle 1 solution is: {surface_area}')

#
# Puzzle 2
#
x_values = [x for x, _, _ in cubes]
y_values = [y for _, y, _ in cubes]
z_values = [z for _, _, z in cubes]
x_min, x_max = min(x_values)-1, max(x_values)+1
y_min, y_max = min(y_values)-1, max(y_values)+1
z_min, z_max = min(z_values)-1, max(z_values)+1

# Use BFS to define a set consisting of all "outside" areas
queue = deque([ (x_min, y_min, z_min) ])
outside = set()
while len(queue) > 0:
    x, y, z = queue.popleft()
    if (x, y, z) in outside: continue
    outside.add((x, y, z))
    neighbors = {(x+1, y, z), (x-1, y, z), (x, y+1, z), (x, y-1, z), (x, y, z+1), (x, y, z-1)} - cubes
    for x, y, z in neighbors:
        if x_min <= x <= x_max and y_min <= y <= y_max and z_min <= z <= z_max: queue.append((x, y, z))

# Rerun test from puzzle 1
surface_area = 0
for x, y, z in cubes:
    neighbors = {(x+1, y, z), (x-1, y, z), (x, y+1, z), (x, y-1, z), (x, y, z+1), (x, y, z-1)}
    surface_area += len(neighbors & outside)

print(f'Puzzle 2 solution is: {surface_area}')