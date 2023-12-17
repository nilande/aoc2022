def get_section_points(section_from, section_to):
    x1, y1 = section_from
    x2, y2 = section_to
    points = set()
    for x in range(min(x1, x2), max(x1, x2)+1):
        for y in range(min(y1, y2), max(y1, y2)+1):
            points.add((x, y))
    return points

def get_set_bounds(point_set):
    x_values = [x for x, y in point_set]
    y_values = [y for x, y in point_set]
    return min(x_values), min(y_values), max(x_values), max(y_values)

def import_rock_structures(rock_structures):
    rock_set = set()
    for rock_structure in rock_structures:
        sections = list(map(lambda x: tuple(map(int, x.split(','))), rock_structure.split(' -> ')))
        for i in range(len(sections)-1):
            section_from, section_to = (sections[i], sections[i+1])
            rock_set |= get_section_points(section_from, section_to)
    return rock_set

def get_resting_place(point_set: set, set_bounds: tuple, x: int, y: int):
    x_min, _, x_max, y_max = set_bounds
    while True:
        if not (x, y+1) in point_set:
            y += 1
        elif not (x-1, y+1) in point_set:
            x -= 1
            y += 1
        elif not (x+1, y+1) in point_set:
            x += 1
            y += 1
        else:
            return x, y
        if not x_min <= x <= x_max: return None
        if not y <= y_max: return None

def get_printable_output(rock_set: set, point_set: set, set_bounds: tuple):
    x_min, y_min, x_max, y_max = set_bounds
    output = ''
    for y in range(y_min, y_max+1):
        for x in range(x_min, x_max+1):
            if (x, y) in rock_set: output += '#'
            elif (x, y) in point_set: output += '\033[33m' + 'o' + '\033[0m'
            else: output += ' '
        output += '\n'
    return output

#
# Process input
#
with open('day 14/input.txt', 'r') as file:
    rock_structures = file.read().splitlines()

#
# Puzzle 1
#
rock_set = import_rock_structures(rock_structures)
set_bounds = get_set_bounds(rock_set)
point_set = rock_set.copy()
acc = 0
while True:
    result = get_resting_place(point_set, set_bounds, 500, 0)
    if result is None: break
    point_set.add(result)
    acc += 1

set_bounds = get_set_bounds(point_set)
print(get_printable_output(rock_set, point_set, set_bounds))

print(f'Puzzle 1 soltuion is: {acc}')

#
# Puzzle 2
#
floor_y = set_bounds[3]+2
floor_x1 = 500 - floor_y
floor_x2 = 500 + floor_y
rock_structures.append(f'{floor_x1},{floor_y} -> {floor_x2},{floor_y}')
rock_set = import_rock_structures(rock_structures)
set_bounds = get_set_bounds(rock_set)
point_set = rock_set.copy()
acc = 0
while True:
    acc += 1
    result = get_resting_place(point_set, set_bounds, 500, 0)
    point_set.add(result)
    if result == (500, 0): break

set_bounds = get_set_bounds(point_set)
print(get_printable_output(rock_set, point_set, set_bounds))

print(f'Puzzle 2 soltuion is: {acc}')
