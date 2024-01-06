import functools, re
from collections import deque

#
# Classes
#
class Valve:
    def __init__(self, init_string: str) -> None:
        name, flow_rate, tunnels = next(iter(re.findall(r'Valve (..) has flow rate=(\d+); tunnels? leads? to valves? (.*)', init_string)))
        self.name = name
        self.flow_rate = int(flow_rate)
        self.tunnels = {t: None for t in tunnels.split(', ')}

    def __repr__(self) -> str:
        return f'{self.name}*'

    def update_tunnels(self, tunnels: dict) -> None:
        for t in self.tunnels: self.tunnels[t] = tunnels[t]

    def setid(self, id: int) -> None:
        self.id = id

    def find_paths(self) -> None:
        queue = deque([ (self, 0) ])
        visited = set()
        paths = {}
        while len(queue) > 0:
            obj, steps = queue.popleft()
            if obj in visited: continue
            visited.add(obj)
            if obj != self and obj.flow_rate > 0: paths[obj.id] = steps
            for t in obj.tunnels.values(): queue.append((t, steps+1))
        return paths


#
# Process input
#
with open('day 16/input.txt') as file:
    valves = {v.name: v for v in map(lambda x: Valve(x), file.read().splitlines())}
id = 1
valves['AA'].setid(id)
for v in valves.values():
    v.update_tunnels(valves)
    if v.flow_rate > 0 and v.name != 'AA':
        id <<= 1
        v.setid(id)

# Build a quick lookup dictionaries with steps and flow rates like this:
# [from_mask][to_mask] = steps, [id_mask] = flow_rate
valve_paths = {}
valve_flowrates = {}
for v in valves.values():
    if v.flow_rate > 0 or v.name == 'AA':
        valve_paths[v.id] = v.find_paths()
        valve_flowrates[v.id] = v.flow_rate

#
# Puzzle 1
#
@functools.cache
def open_valves(id: int, valves_open: int, t_rem: int) -> int:
    # Open the current valve (time for opening added in the move here)
    valves_open &= ~id
    # Return 0 if we are out of time
    if t_rem <= 0: return 0
    valves_not_tested = valves_open
    next_id = 1
    best_val = 0
    while valves_not_tested != 0:
        if next_id & valves_not_tested:
            # Test next valve
            next_val = open_valves(next_id, valves_open, t_rem - valve_paths[id][next_id]-1)
            if next_val > best_val: best_val = next_val
            valves_not_tested &= ~next_id
        next_id <<= 1
    return valve_flowrates[id] * t_rem + best_val

print(f'Puzzle 1 solution is: {open_valves(1, 2**len(valve_paths)-1, 30)}')


#
# Puzzle 2
#
@functools.cache
def open_valves(ids: tuple, valves_open: int, t_rems: tuple) -> int:
    id, id2 = ids
    t_rem, t_rem2 = t_rems

    # Open the current valve (time for opening added in the move here)
    valves_open &= ~id
    # Return 0 if we are out of time
    if t_rem <= 0: return 0

    # Swap next move if actor #2 has more time remaining
    if t_rem2 > t_rem:
        t_rem, t_rem2 = t_rem2, t_rem
        id, id2 = id2, id

    valves_not_tested = valves_open
    next_id = 1
    best_val = 0
    while valves_not_tested != 0:
        if next_id & valves_not_tested:
            # Test next valve
            next_val = open_valves((next_id, id2), valves_open, (t_rem - valve_paths[id][next_id]-1, t_rem2))
            if next_val > best_val: best_val = next_val
            valves_not_tested &= ~next_id
        next_id <<= 1
    return valve_flowrates[ids[0]] * t_rems[0] + best_val

print(f'Puzzle 2 solution is: {open_valves((1, 1), 2**len(valve_paths)-1, (26, 26))}')