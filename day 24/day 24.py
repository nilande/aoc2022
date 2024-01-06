from collections import deque

#
# Classes
#
class Blizzard:
    def __init__(self, pos: complex, dir: complex, width: int, height: int) -> None:
        self.pos = pos
        self.dir = dir
        self.width = width
        self.height = height

    def move(self) -> None:
        self.pos = self.pos + self.dir
        if int(self.dir.real) != 0 and not (0 < int(self.pos.real) < self.width-1): self.pos -= (self.width-2) * self.dir
        elif int(self.dir.imag) != 0 and not (0 < int(self.pos.imag) < self.height-1): self.pos -= (self.height-2) * self.dir


class ValleyMap:
    def __init__(self, map_string: str) -> None:
        self.width = map_string.find('\n') + 1
        self.height = -(len(map_string)//-self.width)
        
        self.walkable = set()
        self.walls = set()
        self.blizzards = []
        for i, c in enumerate(map_string):
            pos = i%self.width + i//self.width*1j
            match c:
                case '.': self.walkable.add(pos)
                case '>': self.blizzards.append(Blizzard(pos, 1, self.width-1, self.height))
                case '<': self.blizzards.append(Blizzard(pos, -1, self.width-1, self.height))
                case '^': self.blizzards.append(Blizzard(pos, -1j, self.width-1, self.height))
                case 'v': self.blizzards.append(Blizzard(pos, 1j, self.width-1, self.height))
                case '#': self.walls.add(pos)
        for b in self.blizzards: self.walkable.add(b.pos)
        self.blizzard_locations = self.get_blizzard_locations()
        self.blizzard_moves = 0
        self.start = 1+0j
        self.finish = self.width-3 + (self.height-1)*1j

    def draw(self) -> None:
        map_string = ''
        blizzards = {b.pos: b.dir for b in self.blizzards}
        for r in range(self.height):
            for c in range(self.width-1):
                pos = c + r*1j
                if pos in self.walls: map_string += '#'
                elif pos in blizzards:
                    match blizzards[pos]:
                        case 1: map_string += '>'
                        case -1: map_string += '<'
                        case 1j: map_string += 'v'
                        case -1j: map_string += '^'
                else: map_string += ' '
            map_string += '\n'
        print(map_string)

    def get_blizzard_locations(self) -> set:
        return {b.pos for b in self.blizzards}

    def move_blizzards(self) -> None:
        for b in self.blizzards: b.move()
        self.blizzard_locations = self.get_blizzard_locations()
        self.blizzard_moves += 1


#
# Process input
#
with open('day 24/input.txt') as file:
    valley_map = ValleyMap(file.read())

#
# Puzzle 1
#
queue = deque([ (valley_map.start, '') ])
visited = set()
while len(queue) > 0:
    pos, path = queue.popleft()
    if pos == valley_map.finish: break
    if len(path) != valley_map.blizzard_moves:
        valley_map.move_blizzards()
        visited.clear()
    if pos in visited or pos in valley_map.blizzard_locations: continue
    visited.add(pos)
    next_steps = {(pos+1, 'R'), (pos-1, 'L'), (pos+1j, 'D'), (pos-1j, 'U'), (pos, '.')} 
    for next_pos, step in next_steps:
        if next_pos in valley_map.walkable: queue.append((next_pos, path + step))

print(f'Puzzle 1 solution is: {valley_map.blizzard_moves}')

#
# Puzzle 2 quick and dirty
#

# Go home
queue = deque([ (pos, path) ])
visited = set()
while len(queue) > 0:
    pos, path = queue.popleft()
    if pos == valley_map.start: break
    if len(path) != valley_map.blizzard_moves:
        valley_map.move_blizzards()
        visited.clear()
    if pos in visited or pos in valley_map.blizzard_locations: continue
    visited.add(pos)
    next_steps = {(pos+1, 'R'), (pos-1, 'L'), (pos+1j, 'D'), (pos-1j, 'U'), (pos, '.')} 
    for next_pos, step in next_steps:
        if next_pos in valley_map.walkable: queue.append((next_pos, path + step))

# Go back
queue = deque([ (pos, path) ])
visited = set()
while len(queue) > 0:
    pos, path = queue.popleft()
    if pos == valley_map.finish: break
    if len(path) != valley_map.blizzard_moves:
        valley_map.move_blizzards()
        visited.clear()
    if pos in visited or pos in valley_map.blizzard_locations: continue
    visited.add(pos)
    next_steps = {(pos+1, 'R'), (pos-1, 'L'), (pos+1j, 'D'), (pos-1j, 'U'), (pos, '.')} 
    for next_pos, step in next_steps:
        if next_pos in valley_map.walkable: queue.append((next_pos, path + step))
    
print(f'Puzzle 2 solution is: {valley_map.blizzard_moves}')