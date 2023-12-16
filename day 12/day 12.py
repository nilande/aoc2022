import time

#
# Process input
#
with open('day 12/input.txt', 'r') as file:
    heightmap = file.read()
width = heightmap.find('\n') + 1
height = (len(heightmap) + 1) // width

#
# Functions
#
def to_tile(pos):
    return (pos // width, pos % width)

def to_index(tile):
    row, col = tile
    return row * width + col

def is_tile_move_valid(from_tile, to_tile, reverse=False):
    row, col = to_tile
    if 0 <= col < width-1 and 0 <= row < height:
        from_tile_char = heightmap[to_index(from_tile)].replace('S', 'a').replace('E', 'z')
        to_tile_char = heightmap[to_index(to_tile)].replace('S', 'a').replace('E', 'z')
        if reverse == False and ord(to_tile_char) - ord(from_tile_char) <= 1: return True
        elif reverse == True and ord(from_tile_char) - ord(to_tile_char) <= 1: return True
    return False

def find_shortest_path(from_tile, to_tile):
    search_queue = [ (from_tile, from_tile) ]
    reached_tiles = dict()
    while len(search_queue) > 0:
        search_tile, prev_tile = search_queue.pop(0)
        if not is_tile_move_valid(prev_tile, search_tile): continue
        if search_tile in reached_tiles.keys(): continue
        reached_tiles[search_tile] = prev_tile
        if search_tile == to_tile: break
        next_tiles = [ (search_tile[0]+1, search_tile[1]), (search_tile[0]-1, search_tile[1]), (search_tile[0], search_tile[1]+1), (search_tile[0], search_tile[1]-1) ]
        for next_tile in next_tiles: search_queue.append((next_tile, search_tile))
    
    shortest_path = [ to_tile ]
    while to_tile != from_tile:
        to_tile = reached_tiles[to_tile]
        shortest_path.append(to_tile)
    return shortest_path

def find_shortest_path_to_a(from_tile):
    search_queue = [ (from_tile, from_tile) ]
    reached_tiles = dict()
    while len(search_queue) > 0:
        search_tile, prev_tile = search_queue.pop(0)
        if not is_tile_move_valid(prev_tile, search_tile, reverse=True): continue
        if search_tile in reached_tiles.keys(): continue
        reached_tiles[search_tile] = prev_tile
        if heightmap[to_index(search_tile)] == 'a': break
        next_tiles = [ (search_tile[0]+1, search_tile[1]), (search_tile[0]-1, search_tile[1]), (search_tile[0], search_tile[1]+1), (search_tile[0], search_tile[1]-1) ]
        for next_tile in next_tiles: search_queue.append((next_tile, search_tile))
    
    shortest_path = [ search_tile ]
    while search_tile != from_tile:
        search_tile = reached_tiles[search_tile]
        shortest_path.append(search_tile)
    return shortest_path

def get_colored_heightmap(path: list, endpoints: list):
    heightmap_col = heightmap
    path_indexes = [to_index(tile) for tile in path]
    endpoint_indexes = [to_index(tile) for tile in endpoints]
    indexes = sorted(path_indexes + endpoint_indexes, reverse=True)
    for index in indexes:
        if index in path_indexes: heightmap_col = heightmap_col[:index] + '\033[91m' + heightmap_col[index:index+1] + '\033[0m' + heightmap_col[index+1:]
        else: heightmap_col = heightmap_col[:index] + '\033[93m' + heightmap_col[index:index+1] + '\033[0m' + heightmap_col[index+1:]

    return heightmap_col

#
# Puzzle 1
#
from_tile = to_tile(heightmap.find('S'))
to_tile = to_tile(heightmap.find('E'))
shortest_path = find_shortest_path(from_tile, to_tile)
heightmap_col = get_colored_heightmap(shortest_path[1:-1], [shortest_path[0], shortest_path[-1]])
print(heightmap_col)
print(f'Puzzle 1 solution is: {len(shortest_path)-1}')

#
# Puzzle 2
#
shortest_path = find_shortest_path_to_a(to_tile)
heightmap_col = get_colored_heightmap(shortest_path[1:-1], [shortest_path[0], shortest_path[-1]])
print(heightmap_col)
print(f'Puzzle 2 solution is: {len(shortest_path)-1}')
