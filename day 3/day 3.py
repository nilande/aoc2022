#
# Process input
#
with open('day 3/input.txt', 'r') as file:
    content = file.read()

#
# Puzzle 1
#
acc = 0
for backpack in content.splitlines():
    items = len(backpack) // 2
    
    # Create two sets, one per compartment
    first = set(backpack[:items])
    second = set(backpack[items:])
    common = next(iter(first.intersection(second)))
    
    if ord(common) >= ord('a'):
        acc += ord(common) - ord('a') + 1
    else:
        acc += ord(common) - ord('A') + 27

print("Puzzle 1 solution is:", acc)

#
# Puzzle 2
#
acc = 0
elves = content.splitlines()
for i in range(0, len(elves), 3):
    elfOne = set(elves[i])
    elfTwo = set(elves[i+1])
    elfThree = set(elves[i+2])
    common = next(iter(elfOne.intersection(elfTwo).intersection(elfThree)))
    
    if ord(common) >= ord('a'):
        acc += ord(common) - ord('a') + 1
    else:
        acc += ord(common) - ord('A') + 27

print("Puzzle 2 solution is:", acc)
