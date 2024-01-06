#
# Classes
#
class Number:
    def __init__(self, num: int, mod: int) -> None:
        self.num = num
        self.mod = mod

    def __repr__(self) -> str:
        return str(self.num)

    def connect(self, l: 'Number', r: 'Number') -> None:
        """Creates linked list with neighbors"""
        self.l = l
        self.r = r

    def mix(self) -> None:
        """Moves the elemenent across the linked list"""

        # Connect old neighbors
        self.l.r = self.r
        self.r.l = self.l

        # Figure out new place to inject myself
        new_l = self.l
        new_r = self.r
        for i in range(0, self.num%(self.mod-1)):
            new_l = new_r
            new_r = new_r.r

        # Inject myself between new neigbors
        new_l.r = self
        new_r.l = self
        self.l = new_l
        self.r = new_r

#
# Helper functions
#
def enumerate_linked_list(sequence: list, origin = int) -> list:
    """Enumerates the linked list, starting at the value 'origin'"""
    origin = [n for n in sequence if origin == n.num][0]
    result = [ origin ]
    for i in range(len(sequence)-1): result.append(result[-1].r)
    return result

#
# Process input
#
with open('day 20/input.txt') as file:
    seq = list(map(int, file.read().splitlines()))
    sequence = list(map(lambda x: Number(x, len(seq)), seq))

#
# Puzzle 1
#

# Connect the linked list
sequence_len = len(sequence)
for i, n in enumerate(sequence):
    n.connect(sequence[(i-1)%sequence_len], sequence[(i+1)%sequence_len])

# Mix the list
for s in sequence: s.mix()

# Figure out the result
acc = 0
new_sequence = enumerate_linked_list(sequence, 0)
for i in range(1000, 3001, 1000):
    acc += new_sequence[i % sequence_len].num

print(f'Puzzle 1 solution is: {acc}')

#
# Puzzle 2
#
ENCRYPTION_KEY = 811589153
sequence = list(map(lambda x: Number(ENCRYPTION_KEY*x, len(seq)), seq))

for i, n in enumerate(sequence):
    n.connect(sequence[(i-1)%sequence_len], sequence[(i+1)%sequence_len])

for i in range(10):
    # Mix the list
    for s in sequence: s.mix()

# Figure out the result
acc = 0
new_sequence = enumerate_linked_list(sequence, 0)
for i in range(1000, 3001, 1000):
    acc += new_sequence[i % sequence_len].num

print(f'Puzzle 2 solution is: {acc}')