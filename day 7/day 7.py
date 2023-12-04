import re

#
# Process input
#
with open('day 7/input.txt', 'r') as file:
    content = file.read()

tree = {}
path = []
current = tree

for command in content.split('$ ')[1:]:
    lines = command.strip().split('\n')
    
    argv = lines[0].split()

    match argv[0]:
        case 'cd':
            match argv[1]:
                case '/':
                    path = []
                case '..':
                    path.pop()
                case _:
                    path.append(argv[1])

            # Navigate to new path
            current = tree
            for i in range(len(path)):
                current = current[path[i]]
        case 'ls':
            # Loop through results from dir command
            for i in range(1, len(lines)):
                entry = lines[i].split()
                if entry[0] == 'dir':
                    if not entry[1] in current: current[entry[1]] = {}
                else:
                    current[entry[1]] = entry[0]
                
dirSizes = []
def sizeof(dir):
    size = 0
    for entry, contents in dir.items():
        if type(contents) is dict:
            size += sizeof(contents)
        else:
            size += int(contents)

    dirSizes.append(size) # Add folder size to list of folder sizes
    return size

#
# Puzzle 1
#
diskUsed = sizeof(tree)
print("Puzzle 1 solution is:", sum(i for i in dirSizes if i <= 100000))

#
# Puzzle 2
#
diskCapacity = 70000000
diskFree = diskCapacity - diskUsed
diskRequired = 30000000
diskToClean = diskRequired - diskFree
print("Puzzle 2 solution is:", min(i for i in dirSizes if i >= diskToClean))