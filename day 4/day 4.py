#
# Process input
#
with open('day 4/input.txt', 'r') as file:
    content = file.read()

#
# Puzzle 1
#
acc = 0
for line in content.splitlines():
    s1, s2 = line.split(',')
    l1, r1 = map(int, s1.split('-'))
    l2, r2 = map(int, s2.split('-'))

    if l1 <= l2 and r1 >= r2:
        acc += 1
    elif l1 >= l2 and r1 <= r2:
        acc += 1

print("Puzzle 1 solution is:", acc)

#
# Puzzle 2
#
acc = 0
for line in content.splitlines():
    s1, s2 = line.split(',')
    l1, r1 = map(int, s1.split('-'))
    l2, r2 = map(int, s2.split('-'))

    if l1 <= l2 and r1 >= r2:
        acc += 1
    elif l1 >= l2 and r1 <= r2:
        acc += 1
    elif l1 <= l2 and r1 >= l2:
        acc += 1
    elif l2 <= l1 and r2 >= l1:
        acc += 1

print("Puzzle 2 solution is:", acc)

