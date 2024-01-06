import re

#
# Classes
#
class BoardMap:
    FACING_LOOKUP = {
        1: 0,
        1j: 1,
        -1: 2,
        -1j: 3
    }

    def __init__(self, map_string: str, wrap_as_cube: bool = False) -> None:
        # Build list of tiles
        x = 1
        y = 1
        xs = {}
        ys = {}
        self.open_tiles = set()
        self.wall_tiles = set()
        for c in map_string:
            match c:
                case '.':
                    self.open_tiles.add(x+y*1j)
                    xs.setdefault(y, set()).add(x)
                    ys.setdefault(x, set()).add(y)
                case '#':
                    self.wall_tiles.add(x+y*1j)
                    xs.setdefault(y, set()).add(x)
                    ys.setdefault(x, set()).add(y)
                case '\n':
                    y += 1
                    x = 0
            x += 1
        all_tiles = self.open_tiles | self.wall_tiles

        # Identify neighbors
        self.tile_neighbors = {}
        for t in all_tiles:
            x, y = int(t.real), int(t.imag)
            potential_neighbors = [(1, t+1, 1), (-1, t-1, -1), (1j, t+1j, 1j), (-1j, t-1j, -1j)]
            neighbors = {k: (v, d) for k, v, d in potential_neighbors if v in all_tiles}
            if not wrap_as_cube:
                missing = [k for k, v, _ in potential_neighbors if v not in all_tiles]
                for dir in missing:
                    match dir:
                        case 1: neighbors[dir] = (min(xs[y]) + y*1j, dir)
                        case -1: neighbors[dir] = (max(xs[y]) + y*1j, dir)
                        case 1j: neighbors[dir] = (x + min(ys[x])*1j, dir)
                        case -1j: neighbors[dir] = (x + max(ys[x])*1j, dir)
            self.tile_neighbors[t] = neighbors

        # Conduct cube wrapping:
        if wrap_as_cube:
            CUBE_LEN = 50
            for i in range(CUBE_LEN):
                # Input specific wrapping - may need updating if input is different
                self.tile_neighbors[100+(51+i)*1j][1] = (101+i+50j, -1j)
                self.tile_neighbors[101+i+50j][1j] = (100+(51+i)*1j, -1)
                self.tile_neighbors[1+i+101j][-1j] = (51+(51+i)*1j, 1)
                self.tile_neighbors[51+(51+i)*1j][-1] = (1+i+101j, 1j)
                self.tile_neighbors[1+(101+i)*1j][-1] = (51+(50-i)*1j, 1)
                self.tile_neighbors[51+(50-i)*1j][-1] = (1+(101+i)*1j, 1)
                self.tile_neighbors[50+(151+i)*1j][1] = (51+i+150j, -1j)
                self.tile_neighbors[51+i+150j][1j] = (50+(151+i)*1j, -1)
                self.tile_neighbors[150+(1+i)*1j][1] = (100+(150-i)*1j, -1)
                self.tile_neighbors[100+(150-i)*1j][1] = (150+(1+i)*1j, -1)
                self.tile_neighbors[101+i+1j][-1j] = (1+i+200j, -1j)
                self.tile_neighbors[1+i+200j][1j] = (101+i+1j, 1j)
                self.tile_neighbors[51+i+1j][-1j] = (1+(151+i)*1j, 1)
                self.tile_neighbors[1+(151+i)*1j][-1] = (51+i+1j, 1j)

                # # Wrappings for test puzzle cube below. When used the CUBE_LEN should be set to 4
                # self.tile_neighbors[9+i+1j][-1j] = (4-i+5j, 1j)
                # self.tile_neighbors[4-i+5j][-1j] = (9+i+1j, 1j)
                # self.tile_neighbors[9+(i+1)*1j][-1] = (5+i+5j, 1j)
                # self.tile_neighbors[5+i+5j][-1j] = (9+(i+1)*1j, 1)
                # self.tile_neighbors[12+(i+1)*1j][1] = (16+(12-i)*1j, -1)
                # self.tile_neighbors[16+(12-i)*1j][1] = (12+(i+1)*1j, -1)
                # self.tile_neighbors[12+(5+i)*1j][1] = (16-i+9j, 1j)
                # self.tile_neighbors[16-i+9j][-1j] = (12+(5+i)*1j, -1)
                # self.tile_neighbors[5+i+8j][1j] = (9+(12-i)*1j, 1)
                # self.tile_neighbors[9+(12-i)*1j][-1] = (5+i+8j, -1j)
                # self.tile_neighbors[1+i+8j][1j] = (12-i+12j, -1j)
                # self.tile_neighbors[12-i+12j][1j] = (1+i+8j, -1j)
                # self.tile_neighbors[1+(5+i)*1j][-1] = (16-i+12j, -1j)
                # self.tile_neighbors[16-i+12j][1j] = (1+(5+i)*1j, 1)

            # Finally, check if cube wrapping is complete:
            acc = 0
            for t, nb_dict in self.tile_neighbors.items():
                expected_nb = {1+0j, -1+0j, 0+1j, 0-1j}
                for nb in expected_nb:
                    if not nb in nb_dict:
                        acc += 1
                        print(f'WARNING: Position {t} is missing wrapping in direction {nb}')
            if acc > 0: print(f'ERROR: Missing wrappings for {acc} coordinates')


        self.start_pos = min(xs[1]) + 1j
        self.start_dir = 1

    def follow_path(self, path_string: str) -> tuple:
        instructions = re.findall(r'(\d+|R|L)', path_string)
        pos = self.start_pos
        dir = self.start_dir
        for instruction in instructions:
            match instruction:
                case 'L': dir *= -1j
                case 'R': dir *= 1j
                case n:
                    for i in range(int(n)):
                        new_pos, new_dir = self.tile_neighbors[pos][dir]
                        if not new_pos in self.open_tiles: break
                        pos = new_pos
                        dir = new_dir
        return pos, dir
    
    def get_password(self, pos, dir) -> int:
        return 1000 * int(pos.imag) + 4* int(pos.real) + BoardMap.FACING_LOOKUP[dir]

#
# Process input
#
with open('day 22/input.txt') as file:
    map_string, path_string = file.read().split('\n\n')

#
# Puzzle 1
#
board_map = BoardMap(map_string)
pos, dir = board_map.follow_path(path_string.strip())
print(f'Puzzle 1 solution is: {board_map.get_password(pos, dir)}')

#
# Puzzle 2
#
board_map = BoardMap(map_string, wrap_as_cube=True)
pos, dir = board_map.follow_path(path_string.strip())
print(f'Puzzle 2 solution is: {board_map.get_password(pos, dir)}')
