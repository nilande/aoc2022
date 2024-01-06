import time

#
# Classes
#
class ElfMap:
    def __init__(self, map_string: str) -> None:
        width = map_string.find('\n')+1
        self.elves = set()
        for i, c in enumerate(map_string):
            if c == '#': self.elves.add(i%width + i//width*1j)
        self.round_no = 0
        self.directions = [-1j, 1j, -1, 1]
        self.prev_draw_lines = 0

    def __mask_to_braille(self, mask: int) -> int:
        braille_masks = [0x1, 0x2, 0x4, 0x40, 0x8, 0x10, 0x20, 0x80]
        braille_mask = 0
        for i in range(8):
            if mask & 1 << i: braille_mask |= braille_masks[i]
        return chr(0x2800 + braille_mask)

    def __render_set(self, data: set) -> tuple:
        """Renders the contents of a set containing complex coordinates - x is the real value (right is positive) and y is the imaginary part (down is positive)"""
        cols = [int(x.real) for x in data]
        rows = [int(x.imag) for x in data]
        string = ''
        lines = 0
        for r in range(min(rows)//4, -(max(rows)//-4)+1):
            y = r * 4
            for c in range(min(cols)//2, -(max(cols)//-2)+1):
                x = c * 2
                char_mask = 0
                for i in range(8):
                    if x+i//4 + (y+i%4)*1j in data: char_mask |= 1<<i
                string += self.__mask_to_braille(char_mask)
            string += '\n'
            lines += 1
        return string, lines

    def draw(self):
        preamble = f'\033[{self.prev_draw_lines+1}A' if self.prev_draw_lines > 0 else ''
        rendered_set, self.prev_draw_lines = self.__render_set(self.elves)
        print(preamble + rendered_set)
        time.sleep(0.01)

    def get_ground_tiles(self):
        cols = [int(x.real) for x in self.elves]
        rows = [int(x.imag) for x in self.elves]
        width = max(cols) - min(cols) + 1
        height = max(rows) - min(rows) + 1
        return width * height - len(self.elves)
    
    def perform_round(self) -> bool:
        proposed_elves = {}
        next_elves = set()
        for elf in self.elves:
            neighbors = {elf-1-1j, elf-1j, elf+1-1j, elf+1, elf-1, elf-1+1j, elf+1j, elf+1+1j}
            if neighbors.isdisjoint(self.elves): # Don't move unless needed
                next_elves.add(elf)
                continue
            for i in range(4): # Try the four directions
                dir = self.directions[(self.round_no+i) % 4]
                dir_checks = {dir, dir+dir*1j, dir+dir*-1j}
                elf_checks = {elf + d for d in dir_checks}
                if elf_checks.isdisjoint(self.elves): # This direction works, propose it
                    proposed_elves.setdefault(elf+dir, set())
                    proposed_elves[elf+dir].add(elf)
                    break
            else: next_elves.add(elf) # No direction works, stay where you are

        # Accept proposals with 1 elf, others stay
        for proposed_elf, current_elves in proposed_elves.items():
            if len(current_elves) > 1: next_elves |= current_elves
            else: next_elves.add(proposed_elf)

        elves_moved = self.elves != next_elves
        if elves_moved:
            self.round_no += 1
            self.elves = next_elves
            return True
        else:
            return False

#
# Process input
#
with open('day 23/input.txt') as file:
    elf_map = ElfMap(file.read())

#
# Puzzles 1 and 2
#
i = 0
while True:
    i += 1
    moved = elf_map.perform_round()
    if i == 10: ground_tiles = elf_map.get_ground_tiles()
    if not moved: break
    elf_map.draw()

print(f'Puzzle 1 solution is: {ground_tiles}')
print(f'Puzzle 2 solution is: {i}')