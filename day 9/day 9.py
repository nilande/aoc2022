#
# Process input
#
with open('day 9/input.txt', 'r') as file:
    content = file.read().splitlines()

#
# Puzzle 1
#
head = [0, 0]
tail = [0, 0]
tailtrail = set()

for row in content:
    direction, steps = row.split()
    for i in range(int(steps)):
        # Head movement
        match direction:
            case 'R':
                head[0] += 1
            case 'L':
                head[0] -= 1
            case 'D':
                head[1] += 1
            case 'U':
                head[1] -= 1
        
        # Tail movement if not touching
        if abs(head[0]-tail[0]) > 1 or abs(head[1]-tail[1]) > 1:
            if abs(head[0]-tail[0]) > 0 and abs(head[1]-tail[1]) > 0:
                tail[0] += int((head[0]-tail[0])/abs(head[0]-tail[0]))
                tail[1] += int((head[1]-tail[1])/abs(head[1]-tail[1]))
            elif abs(head[0]-tail[0]) > 0: tail[0] += int((head[0]-tail[0])/abs(head[0]-tail[0]))
            else: tail[1] += int((head[1]-tail[1])/abs(head[1]-tail[1]))

        tailtrail.add(tuple(tail))
        
print(f"Puzzle 1 solution is: {len(tailtrail)}")

#
# Puzzle 2
#
rope = [[0, 0] for x in range(10)]
tailtrail = set()

for row in content:
    direction, steps = row.split()
    for i in range(int(steps)):
        # Head movement
        match direction:
            case 'R':
                rope[0][0] += 1
            case 'L':
                rope[0][0] -= 1
            case 'D':
                rope[0][1] += 1
            case 'U':
                rope[0][1] -= 1

        # Iterate over knots
        for j in range(1, 10):
            # Tail movement if not touching
            if abs(rope[j-1][0]-rope[j][0]) > 1 or abs(rope[j-1][1]-rope[j][1]) > 1:
                if abs(rope[j-1][0]-rope[j][0]) > 0 and abs(rope[j-1][1]-rope[j][1]) > 0:
                    rope[j][0] += int((rope[j-1][0]-rope[j][0])/abs(rope[j-1][0]-rope[j][0]))
                    rope[j][1] += int((rope[j-1][1]-rope[j][1])/abs(rope[j-1][1]-rope[j][1]))
                elif abs(rope[j-1][0]-rope[j][0]) > 0: rope[j][0] += int((rope[j-1][0]-rope[j][0])/abs(rope[j-1][0]-rope[j][0]))
                else: rope[j][1] += int((rope[j-1][1]-rope[j][1])/abs(rope[j-1][1]-rope[j][1]))

        tailtrail.add(tuple(rope[9]))

print(f"Puzzle 2 solution is: {len(tailtrail)}")
