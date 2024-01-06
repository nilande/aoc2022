import time, math

#
# Classes
#
class JetPattern:
    LEFT = '<'
    RIGHT = '>'

    def __init__(self, pattern_string: str) -> None:
        self.pattern_string = pattern_string
        self.index = -1

    def pick(self) -> str:
        self.index = (self.index + 1) % len(self.pattern_string)
        return self.pattern_string[self.index]


class Rock:
    SHAPES = [
        [0b1111 <<3],                           # -
        [0b010 <<3, 0b111 <<3, 0b010 <<3],      # +
        [0b111 <<3, 0b100 <<3, 0b100 <<3],      # J
        [0b1 <<3, 0b1 <<3, 0b1 <<3, 0b1 <<3],   # |
        [0b11 <<3, 0b11 <<3]                    # o
    ]

    def __init__(self, rock_no: int, tiles: list, jet_pattern: JetPattern, prev_draw_lines: int = 0) -> None:
        self.bits = Rock.SHAPES[rock_no % 5]
        self.tiles = tiles
        self.jet_pattern = jet_pattern
        self.prev_draw_lines = prev_draw_lines

    def spawn(self, alt_offset: int = 0) -> None:
        self.alt = len(self.tiles) - len(self.bits) + alt_offset
        self.landed = False
        while not self.landed:
            self.push()
            self.drop()
        self.settle()
        # self.draw()

    def push(self) -> None:
        match self.jet_pattern.pick():
            case JetPattern.LEFT:
                bits = [b >>1 for b in self.bits]
                if not self.collides(bits, self.alt): self.bits = bits
            case JetPattern.RIGHT:
                bits = [b <<1 for b in self.bits]
                if not self.collides(bits, self.alt): self.bits = bits
            case _:
                print(f'ERROR IN JET PATTERN')
                exit()

    def drop(self) -> None:
        alt = self.alt - 1
        if not self.collides(self.bits, alt): self.alt = alt
        else: self.landed = True

    def collides(self, bits: list, alt: int) -> bool:
        for i in range(len(bits)):
            if bits[i] & self.tiles[alt + i]: return True
        return False

    def settle(self):
        for i in range(len(self.bits)):
            self.tiles[self.alt + i] |= self.bits[i]

    def draw(self) -> None:
        if self.prev_draw_lines != 0: print(f'\033[{self.prev_draw_lines}A', end='')
        self.prev_draw_lines = len(self.tiles)

        for i, t in enumerate(self.tiles[::-1]):
            alt = len(self.tiles)-(i+1)
            string = ''
            if self.alt <= alt < self.alt+len(self.bits): b = self.bits[alt-self.alt]
            else: b = 0
            while t != 0:
                if t & 1: string += chr(0x2588) * 2
                elif b & 1: string += chr(0x2592) * 2
                else: string += '  '
                t >>= 1
                b >>= 1
            print(string)



class Chamber:
    WALL_TEMPLATE = 0b100000001

    def __init__(self, jet_pattern: JetPattern) -> None:
        self.jet_pattern = jet_pattern
        self.tiles = [ 0b111111111 ]
        self.rock_no = 0
        self.prev_draw_lines = 0

    def spawn_rock(self):
        rock = Rock(self.rock_no, self.tiles, self.jet_pattern, self.prev_draw_lines)
        self.rock_no += 1

        # Create space in chamber
        space_req = 3 + len(rock.bits)
        free_space = self.get_free_space()
        if space_req > free_space: self.tiles += [ Chamber.WALL_TEMPLATE ] * (space_req - free_space)

        # Drop rock
        if space_req < free_space:
            rock.spawn(alt_offset=space_req-free_space)
        else:
            rock.spawn()

        # Save the number of lines drawn by the rock
        self.prev_draw_lines = rock.prev_draw_lines

    def get_rock_height(self) -> int:
        return len(self.tiles) - self.get_free_space() - 1

    def get_free_space(self) -> int:
        free_space = 0
        while self.tiles[-free_space-1] == Chamber.WALL_TEMPLATE:
            free_space += 1
        return free_space

#
# Process input
#
with open('day 17/input.txt') as file:
    jet_pattern = JetPattern(file.read().strip())

#
# Puzzle 1
#
chamber = Chamber(jet_pattern)
for i in range(2022):
    chamber.spawn_rock()

print(f'Puzzle 1 solution is {chamber.get_rock_height()}')

#
# Puzzle 2
#
min_pattern_recurrence = math.lcm(len(jet_pattern.pattern_string), 5)

jet_pattern.index = -1
chamber = Chamber(jet_pattern)

rock_heights = [0]
stack_patterns = ['']
while True:
    for i in range(min_pattern_recurrence):
        chamber.spawn_rock()

    i = chamber.get_rock_height()
    rock_heights.append(i)

    # Determine the shape of the top of the stack
    stack_pattern = ''
    iteration_limit = 100
    while chamber.tiles[i] != 0b111111111 and iteration_limit > 0:
        stack_pattern += chr((chamber.tiles[i] >> 1) & 0b1111111)
        i -= 1
        iteration_limit -= 1

    # Break at first recurrence of the top of stack pattern
    if stack_pattern in stack_patterns:
        stack_patterns.append(stack_pattern)
        break
    else:
        stack_patterns.append(stack_pattern)

# Calculate how many rocks have been dropped and the current tower height
current_rocks = (len(rock_heights)-1) * min_pattern_recurrence
current_height = rock_heights[-1]

# Calculate the size of the increment between patterns reoccur
idx = [i for i, p in enumerate(stack_patterns) if p == stack_pattern]
increment_rocks = (idx[1]-idx[0]) * min_pattern_recurrence
increment_height = rock_heights[idx[1]] - rock_heights[idx[0]]

# Caulculate the number of big increments to apply and apply then
target_rocks = 1000000000000
remaining_rocks = target_rocks - current_rocks
num_increments = remaining_rocks // increment_rocks
current_rocks += num_increments * increment_rocks
current_height += num_increments * increment_height

# Walk the final stretch to the target
remaining_rocks = target_rocks - current_rocks
for i in range(remaining_rocks):
    chamber.spawn_rock()
current_height += chamber.get_rock_height()-rock_heights[-1]

print(f'Puzzle 2 solution is: {current_height}')