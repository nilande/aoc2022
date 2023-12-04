#
# Process input
#
with open('day 6/input.txt', 'r') as file:
    content = file.read()

#
# Puzzle 1
#
for i in range(len(content)-3):
    sequence = content[i:i+4]

    if len(set(sequence)) == 4:
        print("Puzzle 1 solution is:", i+4)
        break

#
# Puzzle 2
#
for i in range(len(content)-13):
    sequence = content[i:i+14]

    if len(set(sequence)) == 14:
        print("Puzzle 2 solution is:", i+14)
        break
