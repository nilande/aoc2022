import re

def get_bounds_and_items_on_row(sensor_data: list, row: int):
    l_bounds = []
    r_bounds = []
    items = set()
    for sensor_x, sensor_y, beacon_x, beacon_y in sensor_data:
        sensor_range = abs(beacon_x - sensor_x) + abs(beacon_y - sensor_y)
        sensor_range_on_row = sensor_range - abs(row - sensor_y)
        if sensor_range_on_row < 0: continue
        l_bounds.append(sensor_x - sensor_range_on_row)
        r_bounds.append(sensor_x + sensor_range_on_row)
        if beacon_y == row: items.add(beacon_x)
        if sensor_y == row: items.add(sensor_x)

    l_bounds.sort()
    r_bounds.sort()
    return(l_bounds, r_bounds, items)

def count_positions(l_bounds: list, r_bounds: list, items: set):
    all_bounds = sorted(l_bounds + r_bounds)
    sensor_level = 0
    acc = 0
    active_range_start = int()
    for bound in all_bounds:
        if len(l_bounds) > 0 and bound == l_bounds[0]:
            l_bounds.pop(0)
            sensor_level += 1
            if sensor_level == 1: active_range_start = bound
        elif bound == r_bounds[0]:
            r_bounds.pop(0)
            sensor_level -= 1
            if sensor_level == 0:
                acc += bound - active_range_start + 1
                acc -= sum(active_range_start <= item <= bound for item in items)

    return acc

#
# Process input
#
with open('day 15/input.txt', 'r') as file:
    content = file.read()
sensor_data = list(map(lambda x: tuple(map(int, x)), re.findall(r'x=(-?\d+), y=(-?\d+).*x=(-?\d+), y=(-?\d+)', content, re.MULTILINE)))

#
# Puzzle 1
#
l_bounds, r_bounds, items = get_bounds_and_items_on_row(sensor_data, 2000000)
num_positions = count_positions(l_bounds, r_bounds, items)
print(f'Puzzle 1 solution is: {num_positions}')

#
# Puzzle 2
#
# This is not even the prettiest of bruteforce solutions... ¯\_(ツ)_/¯
for row in range(0, 4000000+1):
    l_bounds, r_bounds, _ = get_bounds_and_items_on_row(sensor_data, row)
    for i in range(len(l_bounds)):
        if l_bounds[i] < 0: l_bounds[i] = 0
        if r_bounds[i] < 0: r_bounds[i] = 0
        if l_bounds[i] > 4000000: l_bounds[i] = 4000000
        if r_bounds[i] > 4000000: r_bounds[i] = 4000000
    if count_positions(l_bounds, r_bounds, set()) != 4000001: break
l_bounds, r_bounds, _ = get_bounds_and_items_on_row(sensor_data, row)
for l_bound in l_bounds:
    if l_bound-2 in r_bounds: break
result = (l_bound-1) * 4000000 + row
print(f'Puzzle 2 solution is: {result}')