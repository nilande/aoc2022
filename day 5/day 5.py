import re

#
# Process input
#
with open('day 5/input.txt', 'r') as file:
    content = file.read()

#
# Puzzle 1
#

# Manually setting up boxes from input file, can't be bothered to build an interpreter
stacks = {
    '1': ['W', 'M', 'L', 'F'],
    '2': ['B', 'Z', 'V', 'M', 'F'],
    '3': ['H', 'V', 'R', 'S', 'L', 'Q'],
    '4': ['F', 'S', 'V', 'Q', 'P', 'M', 'T', 'J'],
    '5': ['L', 'S', 'W'],
    '6': ['F', 'V', 'P', 'M', 'R', 'J', 'W'],
    '7': ['J', 'Q', 'C', 'P', 'N', 'R', 'F'],
    '8': ['V', 'H', 'P', 'S', 'Z', 'W', 'R', 'B'],
    '9': ['B', 'M', 'J', 'C', 'G', 'H', 'Z', 'W']
}
regex = '^move (\d+) from (\d) to (\d)'

moves = re.findall(regex, content, re.MULTILINE)

for move in moves:
    (num, moveFrom, moveTo) = move
    for i in range(int(num)):
        stacks[moveTo].append(stacks[moveFrom].pop())

boxes = ''
for i in range(9):
    boxes += stacks[str(i+1)].pop()

print("Puzzle 1 solution is:", boxes)

#
# Puzzle 2
#

# Manually setting up boxes from input file, can't be bothered to build an interpreter
stacks = {
    '1': ['W', 'M', 'L', 'F'],
    '2': ['B', 'Z', 'V', 'M', 'F'],
    '3': ['H', 'V', 'R', 'S', 'L', 'Q'],
    '4': ['F', 'S', 'V', 'Q', 'P', 'M', 'T', 'J'],
    '5': ['L', 'S', 'W'],
    '6': ['F', 'V', 'P', 'M', 'R', 'J', 'W'],
    '7': ['J', 'Q', 'C', 'P', 'N', 'R', 'F'],
    '8': ['V', 'H', 'P', 'S', 'Z', 'W', 'R', 'B'],
    '9': ['B', 'M', 'J', 'C', 'G', 'H', 'Z', 'W']
}
regex = '^move (\d+) from (\d) to (\d)'

moves = re.findall(regex, content, re.MULTILINE)

for move in moves:
    (num, moveFrom, moveTo) = move
    # Trickery - let's keep popping one at a time but from the bottom of the stack being picked up :)
    for i in range(-int(num),0):
        stacks[moveTo].append(stacks[moveFrom].pop(i))

boxes = ''
for i in range(9):
    boxes += stacks[str(i+1)].pop()

print("Puzzle 2 solution is:", boxes)

